import os
import subprocess
from uuid import uuid4
import re
import numpy as np
from Bio import SeqIO
from .utils import f_ext, guess_target_msa_format, AVAIL_FORMAT, hash_file
import shutil
import json

import logging
logger = logging.getLogger('msafLogger')

from .threader import build_msa_pipeline
from .errors import *
import concurrent.futures
from .chai import build_pqt

CHAIN_ID = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class DB_manager:
    extensions = ["_h", "_h.index", ".lookup", ".index"]
    @staticmethod
    def is_valid_format(ext):
        """Alignment file extension check"""
        return ext in AVAIL_FORMAT
    @staticmethod
    def volume_map(root, files):
        prefixes = list( map(lambda x:x.replace('_h.index', ''), 
                       filter(lambda fname:fname.endswith('_h.index'), files)
                    ) )
        for prefix in prefixes:
            db_def = {'name':prefix, 'location':root}
            for ext in DB_manager.extensions:
                if not f"{prefix}{ext}" in files:
                    raise DB_InitError(f"Missing {ext} file for {prefix}")
            logger.debug(f"Adding database '{prefix}'")
            yield db_def
    
    def register(self, location):      
        for root, dirs, files in os.walk(location):
            logger.debug(f"[DB_manager:register]{root}, {dirs}, {files}")            
            for db_ref in DB_manager.volume_map(root, files):
                if db_ref['name'] in self.registry:
                    raise DB_InitError(f"Multiple definitions for database {db_ref['name']}")
                self.registry[ db_ref['name'] ] = db_ref
            for sub_folders in dirs:
                self.register(sub_folders)
    def get_db_endpoint(self, db_label):
        if not db_label in self.registry:
            raise DB_QueryError(f"Database target {db_label} not found")    
        return os.path.join(self.registry[db_label]['location'], self.registry[db_label]['name'])
                
    def __init__(self, exec_config, root_dir,  *args):
        self.exec_mmseqs = exec_config['mmseqs']
        self.exec_mafft  = exec_config['mafft']
        self.query_file_chain_map = {}
        self.jobs = []

        if not os.access(self.exec_mmseqs, os.X_OK):
            raise DB_InitError(f"Can't execute '{self.exec_mmseqs}'")
        if not os.access(self.exec_mafft, os.X_OK):
            raise DB_InitError(f"Can't execute '{self.exec_mafft}'")


        self.uuid = str( uuid4() )[:7]
        if not os.path.isabs(root_dir):
             raise DB_InitError(f"root directory '{root_dir}' must be absolute")
        if not os.path.exists(root_dir):
            raise DB_InitError(f"root directory '{root_dir}' doesnt exist")

        self.cache_dir = os.path.join(root_dir, self.uuid)
        try :
            os.mkdir(self.cache_dir)
        except Exception as e:
            raise DB_InitError(f"Can't create cache at root directory '{self.cache_dir}'")
                   
        self.registry =  {}
        for loc in args:            
            self.register(loc)
    def get_chain_id(self, query_file):
        """
        get/set chain id of a query file based on its contenthash
        """
        k = hash_file(query_file)
        if not k in self.query_file_chain_map:
            self.query_file_chain_map[k] = CHAIN_ID[len(self.query_file_chain_map)]
        return self.query_file_chain_map[k]
    def iter_chain_id(self):
        for k in self.query_file_chain_map:
            yield self.query_file_chain_map[k]
    
    def get_job_auth(self, query_file, database_name):
        """ register a query hash, database tuple
        """
        k = hash_file(query_file)
        for (q, db) in self.jobs:
            if q == k and db == database_name:
                return False
        self.jobs.append( (k, database_name) )
        return True

    def queries(self, requests:tuple[str, str, str], output_dir, monomer=False, pdqt=False, max_workers=5):
        self.output_dir = output_dir
        try:
            if os.path.exists(output_dir):
                logger.warning(f"Output directory '{output_dir}' already exists, overwriting")
                shutil.rmtree(output_dir)
            os.mkdir(output_dir)
        except Exception as e:
            raise Query_SetupError(f"Can't create outputdirectory {output_dir}: '{e}'")

        self.requests = [
            { 
                'query_file'  : req[0],
                'database'    : self.get_db_endpoint(req[1]),
                'output_file' : req[2],
                'format'      : guess_target_msa_format(req[2]),
                'cwd'         : self.setup_cwd(req[0]),
                'chainID'     : self.get_chain_id(req[0]) if not monomer else None               
            }
            for i,req in enumerate(requests) if self.get_job_auth(req[0], req[1])
        ]
        logger.debug(f"{self.requests}")
        safe = True
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            _ = [executor.submit(build_msa_pipeline, self.exec_mmseqs, self.exec_mafft, req) for req in self.requests]

            for future in concurrent.futures.as_completed(_):              
                try:
                    data = future.result()
                    results.append(data)
                except Exception as exc:
                    logger.error('%r generated an exception: %s' % (future, exc))
                    safe = False
                else:
                    logger.debug(f"{future} success: {data}")
        
        if not safe:
            logger.error(f"Failed to build all queries MSA, exiting")
            return

        self.queries_postprocess(results, output_dir, monomer)
        if pdqt:
            for folder in self.iter_chain_folder():
                build_pqt(folder)

    def iter_chain_folder(self):
        for chain in self.iter_chain_id():
            yield os.path.join(self.output_dir, chain)

    def queries_postprocess(self, results, output_dir, is_monomer):
        chain_id_map = {}
        for (final_msa, query_h, query_s), request in zip(results, self.requests):
            curr_dir = output_dir
            if not is_monomer:           
                if not request['chainID'] in chain_id_map:
                    chain_id_map[request['chainID']] = {
                        'description': query_h,
                        'sequence': query_s
                    }

                    curr_dir = os.path.join(output_dir, request['chainID'])                    
                    try:
                        os.mkdir(curr_dir)
                    except Exception as e:
                        raise Query_PostProcessError(f"Can't create chain specific output directory '{curr_dir}'")

            logger.debug(f"Copying {final_msa} to {curr_dir}")
            shutil.copy( final_msa, os.path.join(curr_dir, request['output_file']) )
        if not is_monomer:
            json_summary = os.path.join(output_dir, "chain_id_map.json")
            json.dump(chain_id_map, open(json_summary, "w"), indent=4)                    
            logger.debug(f"JSON report saved at {json_summary}")       

    def setup_cwd(self, query_file):        
        cwd  = os.path.join(self.cache_dir, str( uuid4() )[:7])     
        try :
            os.mkdir(cwd)
        except Exception as e:
            raise DB_InitError(f"Can't create query work directory '{cwd}' : '{e}'")

        step0_params = [self.exec_mmseqs, "createdb", query_file, 'queryDB']      
        child = subprocess.run(step0_params, capture_output=True, cwd=cwd)
        if not child.returncode == 0:
            raise DB_QuerySetUpError(child.stderr)
        logger.debug(f"{step0_params} @{cwd} completed")
        
        return cwd

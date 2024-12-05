import os
import subprocess
import shutil
from Bio import SeqIO
from .errors import *
from .utils import mfasta_convert
import logging
logger = logging.getLogger('msafThread')

def build_msa_pipeline(exec_mmseqs, exec_mafft, inputs):
    logger.debug(f"parameters: {inputs}")
    fna_file, query_uuid, query_h, query_s = __mmseqs_step__(exec_mmseqs, inputs['cwd'], inputs['database'])
    #msa_file = __mafft_step__(exex_mafft, fna_file, query_uuid, inputs['format'])
    msa_file = __mafft_step__(exec_mafft, fna_file, inputs['cwd'])

    final_msa = __convert_msa__(msa_file, inputs['cwd'], inputs['format'])
    return final_msa, query_h, query_s

def __mmseqs_step__(exec_mmseqs, cwd, target_db):          
    step1_params = [exec_mmseqs, "search", 'queryDB', target_db, 'resultDB', 'tmp']
        #mmseqs search queryDB ../databases/mmseqs/swissprot resultDB tmp
    step2_params = [exec_mmseqs, "convertalis", 'queryDB', 
                        target_db, 'resultDB', 'resultDB.m8', '--format-output', 'theader,tseq']
        # mmseqs convertalis queryDB ../databases/mmseqs/swissprot resultDB resultDB.m8 --format-output theader,tseq
    
    for cmd_param in [step1_params, step2_params]:
        logger.debug(f"[DB_manager:__query_mmseqs__]{cmd_param} @{cwd}")
        res = subprocess.run(cmd_param, capture_output=True, cwd=cwd)
        if res.returncode != 0:
            raise MMSEQS_RunTimeError( res.stderr.decode() )
        
        query_h, query_s = extract_query(cwd, 'queryDB')
        logger.debug(f"Query parameters '{query_h}' AND '{query_s}'")
        
    res_file = os.path.join(cwd, 'resultDB.m8') 
    if not(os.path.exists(res_file) and os.path.getsize(res_file) > 0):
        raise MMSEQS_RunTimeError(f"Empty or missing resultDB.m8 file @{cwd}")

    #rewrite output file with query on top
    res_nr_file = os.path.join(cwd, 'resultDB_top_query.m8')
    hits_set = set()
    with open(res_nr_file, "w") as fp_out:
        #print(f"'{query_h}\t{query_s}'")
        hits_set.add(f"{query_h}\t{query_s}")
        fp_out.write(f"{query_h}\t{query_s}\n")
        with open(res_file,'r') as fp_in:
            for l in fp_in:
                item = l.rstrip()
                if item in hits_set:
                    logger.debug(f"{item} ALREADY EXIST!!")
                    continue
                #print(f"'{item}'")
                hits_set.add(item)
                fp_out.write(f"{item}\n")
    
    fna_file = os.path.join(cwd, 'resultDB.mfasta')
    try :
        mfasta_convert(res_nr_file, fna_file )
    except Exception as e:
        raise MMSEQS_RunTimeError(e)

    logger.info(f"results wrote in '{fna_file}'")

    return fna_file, 'queryDB', query_h, query_s

def __mafft_step__(exec_mafft, fna_file, cwd, mask=True):
    mali_file = os.path.join(cwd, "results_gaped.a3m")
    res = subprocess.run([exec_mafft, fna_file], capture_output=True, cwd=cwd)
    if res.returncode != 0:
        raise MAFFT_RunTimeError(res.stderr)
    
    with open(mali_file, "w") as fp:
        fp.write(res.stdout.decode())

    if mask:
        with open(mali_file, "r") as fp:           
            content = []
            master  = ''
            n = 0
            for l in fp:
                if l.startswith(">"):
                    n += 1
                    content.append({'header': l, 'n':n, 'seq' : ''})                    
                    continue
                l = l.rstrip()
                content[-1]['seq'] += l
                if n == 1:
                    master += l               
            for d in content:
                d['mask'] = ''.join(  [ c for i,c in enumerate(d['seq']) if master[i] != '-' ] )
        mali_file = os.path.join(cwd, "results_dense.a3m")
        with open(mali_file, "w") as fp:
            for d in content:
                fp.write(f"{d['header']}{d['mask']}\n")              
            
    logger.debug(f"MSA generic file wrote in '{mali_file}'")
    return mali_file

def __convert_msa__(msa_file, cwd, fmt):
    if fmt == 'a3m':
        output = os.path.join(cwd, 'results.a3m')
        shutil.copy(msa_file, os.path.join(cwd, output))
    else:   
        in_records = None
        in_records = SeqIO.parse(msa_file, "fasta")   
        if fmt == 'sto':     
            output = os.path.join(cwd, 'results.sto')
            with open(output, "w") as fp:
                SeqIO.write(in_records, fp, "stockholm")            
            logger.info(f"results converted in '{output}'")
    
    logger.info(f"MSA desired format '{fmt}' converted in '{output}'")
    return output

def extract_query(cwd, q_uuid):
    seq = ''
    header = ''
    
    if not os.path.exists(os.path.join(cwd, q_uuid)):
        raise MMSEQS_RunTimeError(os.path.join(cwd, q_uuid), " does not exist")
    with open(os.path.join(cwd, q_uuid), 'r') as fp:
        seq = fp.read()
    with open(os.path.join(cwd, f"{q_uuid}_h"), 'r') as fp:
        header = fp.read()            
    return header.replace('\n', "").replace('\0', ''), seq.replace('\n', "").replace('\0', '')
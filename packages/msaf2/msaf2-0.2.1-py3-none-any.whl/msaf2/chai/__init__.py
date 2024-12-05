from pathlib import Path
from Bio import SeqIO
import pandas as pd
import re
import logging
logger = logging.getLogger('msafLogger')

class PQT_BuildError(Exception):
    pass

CHAI_DB = ['uniprot', 'uniref90', 'bfd_uniclust', 'mgnify']#, 'query']
def guess_src(file:str):
    filename = Path(file).stem
    curr_pfx = None
    for prefix in CHAI_DB:
        if prefix in filename:
            if not curr_pfx is None:
                logger.warning(f"Multiple guessed sources for {file}")
            curr_pfx = prefix
    if curr_pfx is None:
        logger.warning(f"Could not guess source for {file}, setting default to uniprot")
        curr_pfx = 'uniprot'
    return curr_pfx

def extract_specie(seq_record):
    compiled_uniprot = re.compile(r"OS=([^\s]+ [^\s]+)")
    compiled_uniref = re.compile(r"TaxID=(\d+)")
    m = compiled_uniprot.search(seq_record.description)
    if m:
        return m.group(1)
    m = compiled_uniref.search(seq_record.description)
    if m:
        return m.group(1)
    return ""

def extract_pdqt_record_triplet_stack(a3m_path:str):
    """
    Extract from a3m file, the sequence, pairing key and comment Frames
    First line is assumed to be query
    """
    compiled = re.compile(r"OS=([^\s]+ [^\s]+)")
    in_rec = SeqIO.parse(a3m_path, "fasta")
    
    sequence_stack    = []
    pairing_key_stack = []
    comment_stack     = []
    for seq_record in in_rec:
        comment_stack.append(seq_record.description)
        pairing_key_stack.append(
            extract_specie(seq_record) if pairing_key_stack else ' ')
        sequence_stack.append(''.join(seq_record.seq))

    return sequence_stack, pairing_key_stack, comment_stack

def build_pqt(dir:str):    
    dir_path = Path(dir)
    if not dir_path.is_dir():
        PQT_BuildError(f"Directory {dir} does not exist")

    logger.debug(f"Attempting to merge *.a3m files in {dir} ...")
    mapped_a3m_files = {}
    pdqt_stacks = {
        'sequence' : [],
        'pairing_key' : [],
        'comment' : [],
        'source_database' : []
    }

    for file in dir_path.glob("*.a3m"):
        logger.debug(f"Processing {file} ...")
        curr_stacks = extract_pdqt_record_triplet_stack(file)
        pdqt_stacks['sequence'] += curr_stacks[0]
        pdqt_stacks['pairing_key'] += curr_stacks[1]
        pdqt_stacks['comment'] += curr_stacks[2]
        pdqt_stacks['source_database'] += ['query'] + [guess_src(file)] * (len(curr_stacks[0]) - 1)

    df = pd.DataFrame(pdqt_stacks)
    logger.debug(f"Wrapping following dataframe\n{df.head()}")
    pd.DataFrame.to_parquet(df, dir_path / "aligned.pqt")
    logger.info(f"PQT saved to {dir_path / 'aligned.pqt'}")
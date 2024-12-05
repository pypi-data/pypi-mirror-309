import os
import re
import hashlib

AVAIL_FORMAT=["sto", "a3m"]


def f_ext(fpath):
    _, file_ext = os.path.splitext(fpath)
    return file_ext.replace('.', '')

def apply_blueprint(queries:list[str], bp:dict)-> tuple[ list[tuple[str, str, str]], bool ]:   
    requests = [ (q, db['target'], db['label']) for db in bp['ingredients'] for q in queries ]
    pdqt     = bp['pdqt'] if 'pdqt' in bp else False
    
    return requests, pdqt

def mfasta_convert(from_file, to_file):
    re_line = r'(^.*[\S])[\s]+([\S]+)$'
    
    fasta_str = ''
    header = None
    with open(from_file, 'r') as fp:
        for l in fp:
            m = re.match(re_line, l)
            if not m:
                raise ValueError(f"Output format error:\n{l}")
            fasta_str += f">{m.groups()[0]}\n{m.groups()[1]}\n"       
    with open(to_file, 'w') as fp:
        fp.write(fasta_str)

def guess_target_msa_format(msa_target_file:str):
    ext = f_ext(msa_target_file)
    if not ext in AVAIL_FORMAT:
        raise ValueError(f"Unknown MSA format: {ext}")
    return ext

def hash_file(fpath):
    return hashlib.md5(open(fpath,'rb').read()).hexdigest()
import yaml
import logging
logger = logging.getLogger('msafLogger')

def set_config(fpath):
    """
    Read the config file a shape ....
    """
    config = None
    with open(fpath) as f:
        config = yaml.safe_load(f)
   

    if not config:
        logger.error('No config found')
    
    ## Checking config shape here ...
    return config

def generate_config(fpath):
    default_config = {
        'databases' : ['/path/to/mmseqs/databases_group1',
                        '/path/to/mmseqs/database_group2'], 
        'executables' : {
            'mafft': '/path/to/bin/mafft',
            'mmseqs': '/path/to/bin/mmseqs'
        },
        'settings': {  
            'cache' : '/path/to/msaf/cache'
        },
        'cocktails': {
            'test_chai': {
                'ingredients': [
                    { 'target': 'swissprot', 'label': 'pif.sto' },
                    { 'target': 'uniprot', 'label': 'paf.a3m' }
                ],
                'PDQT':True
            },
            'af2': {
                'ingredients': [
                    { 'target': 'bfd_uniref', 'label': 'bfd_uniref_hits.a3m' },
                    { 'target': 'mgnify', 'label': 'mgnify_hits.sto' },
                    { 'target': 'pdb', 'label': 'pdb_hits.sto' },
                    { 'target': 'uniprot', 'label': 'uniprot_hits.sto' },
                    { 'target': 'uniref90', 'label': 'uniref90_hits.sto' }
                ]
            }
        }
    }
            
    yaml.dump(default_config, open(fpath, 'w'), sort_keys=False)
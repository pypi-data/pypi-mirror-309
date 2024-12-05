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
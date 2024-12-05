from  .config import *
from sys import argv
from .manager import *
from .parser import *
from .logger import configure_logger
from .utils import apply_blueprint
from rich import print

if __name__ == '__main__':

    args   = parser.parse_args()

    logger = configure_logger(args.verbosity)
    config = set_config(args.config)    
    logger.debug(config)
    
    manager = DB_manager(
        config['executables'], config['settings']['cache'], *config['databases'])
   
    if args.list:
        print('Available databases')
        for db in manager.registry:
            print(f"\t- {db}")

    if args.query:
        if not args.bp:
            logger.error("--bp <target database blueprint> is required when --query is provided")
            exit(1)      
        requests, pdqt = apply_blueprint(args.query, config['cocktails'][args.bp])
        manager.queries(requests, args.output, monomer= len(args.query) == 1, pdqt=pdqt)
          
    if args.pdqt:
        build_pqt(args.pdqt[0])
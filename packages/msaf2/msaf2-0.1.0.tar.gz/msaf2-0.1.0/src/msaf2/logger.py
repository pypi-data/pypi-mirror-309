import logging
def configure_logger(level:str = 'INFO'):
    logger = logging.getLogger('msafLogger')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s | %(pathname)s:%(funcName)s:%(lineno)s -  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)

    configure_threader_logger(level)

    return logger

def configure_threader_logger(level):
    logger = logging.getLogger('msafThread')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s [Th:%(threadName)s] | %(pathname)s:%(funcName)s:%(lineno)s -  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
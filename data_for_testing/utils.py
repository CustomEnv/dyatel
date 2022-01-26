import logging


def set_logging_settings(level=logging.INFO):
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.basicConfig(level=level, format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    return logging

import os
import logging


sidebar_page_path = f'file://{os.getcwd()}/data_for_testing/sidebar_page.html'
tabs_page_path = f'file://{os.getcwd()}/data_for_testing/tabs_page.html'


def set_logging_settings(level=logging.INFO):
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.basicConfig(level=level, format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    return logging


available_tabs = ('London', 'Paris', 'Tokyo')

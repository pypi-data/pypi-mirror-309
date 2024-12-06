"""the data in this package is downloaded to a local directory
in the config module the path can be defined and cleaned up
"""

import os
import shutil
import logging


LOGGER = logging.getLogger("chemloader")
LOGGER.setLevel(logging.INFO)

LOGGER.addHandler(logging.StreamHandler())


# define the path to the data directory
_DATA_PATH = os.path.join(os.path.expanduser("~"), "chemloader", "data")


def set_data_path(path):
    """set the path to the data directory"""
    global _DATA_PATH
    _DATA_PATH = path
    LOGGER.info(f"Data path set to {_DATA_PATH}")


def get_data_path(create=True):
    """get the path to the data directory"""
    if create:
        make_data_path()
    return _DATA_PATH


def clean_data_path():
    LOGGER.info(f"Cleaning data path {_DATA_PATH}")
    if os.path.exists(_DATA_PATH):
        shutil.rmtree(_DATA_PATH)


def make_data_path():
    if not os.path.exists(_DATA_PATH):
        LOGGER.info(f"Creating data path {_DATA_PATH}")
        os.makedirs(_DATA_PATH)


MISSMATCH_PREFIX = "missmatched_"

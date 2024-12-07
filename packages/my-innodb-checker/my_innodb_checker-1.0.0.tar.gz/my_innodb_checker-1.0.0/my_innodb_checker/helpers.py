"""
Helper functions
"""

import logging
import sys

DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_FORMAT_DEBUG = "[%(asctime)s][%(levelname)-8s]: %(message)s"


def init_logger(name: str, level: str) -> None:
    """
    Function to setup logger
    :param str name: Name of logger
    :param str level: Level name
    :rtype: None
    :return: None
    """

    try:
        logging._checkLevel(level=level.upper())  # type: ignore
    except ValueError:
        logging.error("Level %s doesn't exist", level)
        sys.exit(1)
    set_level = logging.getLevelName(level.upper())
    formater = logging.Formatter(
        DEFAULT_LOG_FORMAT_DEBUG, datefmt=DEFAULT_LOG_DATE_FORMAT
    )
    logger = logging.getLogger(name=name)
    logger.setLevel(level=set_level)
    con = logging.StreamHandler()
    con.setFormatter(fmt=formater)
    con.setLevel(level=set_level)
    logger.addHandler(con)

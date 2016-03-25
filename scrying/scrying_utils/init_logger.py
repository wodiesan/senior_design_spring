#!/usr/bin/env python
"""
Init logging to console and .log files.

Part of ELEC4500 Senior Electronic Design I, Spring 2016
Dept. of Electrical Engineering and Technology
Wentworth Institute of Technology.
"""
import logging
import os.path
import posixpath


def checkdir(path):
    '''Ensure that the path doesn't contain trailing slashes.'''
    path = posixpath.normpath(path)
    return not path.startswith(('/', '../'))


def init_logger(log_name, out_dir, user_log, dev_log):
    '''Setup logging levels for console and files, followed by respective handlers.
    DEBUG: User-level data regarding init and config details (ex: resolution).
    INFO: User-level data regarding objects detected.
    WARNING: User level data that triggers notification to e-mail.
    ERROR: Dev-level information regarding errors.
    CRITICAL: Dev-level oh-gods-why-is-this-happening.'''
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    logging_msg = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Check for trailing slashes in the user-supplied directories.
    if not (checkdir(out_dir) and checkdir(user_log) and checkdir(user_log)):
        print 'Path contains trailing slashes. Aborting.'
    else:
        user_log_dir = os.path.join(out_dir, user_log)
        dev_log_dir = os.path.join(out_dir, dev_log)

    # Init console handler.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(logging_msg)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Init user-level file handler.
    user_handler = logging.FileHandler(os.path.join(user_log_dir))
    user_handler.setLevel(logging.DEBUG)
    user_formatter = logging.Formatter(logging_msg)
    user_handler.setFormatter(user_formatter)
    logger.addHandler(user_handler)

    # Init dev-level file handler.
    dev_handler = logging.FileHandler(os.path.join(dev_log_dir))
    dev_handler.setLevel(logging.ERROR)
    dev_formatter = logging.Formatter(logging_msg)
    dev_handler.setFormatter(dev_formatter)
    logger.addHandler(dev_handler)

    return logger

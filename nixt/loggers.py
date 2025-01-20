# This file is placed in Public Domain.


"logging"


import logging.handlers
import logging
import os
import pathlib


from .persist import cdir, logdir
from .runtime import later


LEVELS = {
          'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
         }


datefmt      = '%H:%M:%S'
format_large = "%(asctime)-8s %(message)-8s %(module)s.%(lineno)s %(threadName)-10s"
format       = "%(message)-8s"
formatter    = logging.Formatter(format_large)
p            = os.path.join


def loglevel(loglevel="error", disk=True):
    logger = logging.getLogger("")
    formatter = logging.Formatter(format, datefmt=datefmt)
    level = LEVELS.get(str(loglevel).lower(), logging.NOTSET)
    filehandler = None
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    if disk:
        logfile = p(logdir(), "nixt.log")
        cdir(logfile)
        pathlib.Path(logfile).touch()
        try:
            filehandler = logging.handlers.TimedRotatingFileHandler(p(logdir(), "nixt.log"), 'midnight')
        except Exception as ex:
            later(ex)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(level)
    logger.addHandler(ch)
    if disk and filehandler:
        ch.setFormatter(formatter)
        filehandler.setLevel(level)
        logger.addHandler(filehandler)
    return logger


loglevel("critical")


def __dir__():
    return (
        'loglevel',
    )

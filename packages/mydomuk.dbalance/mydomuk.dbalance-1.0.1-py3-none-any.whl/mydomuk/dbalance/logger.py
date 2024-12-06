import logging
from enum import Enum

applog = logging.getLogger("dbalance")

class LOGLEVEL(Enum):
    LEVEL_INFO = logging.INFO
    LEVEL_DEBUG = logging.DEBUG
    LEVEL_CRITICAL = logging.CRITICAL
    LEVEL_WARNING = logging.WARNING
    LEVEL_VERBOSE = -1
    LEVEL_NOTSET = logging.NOTSET


_isdebug: bool = False
_curlevel: LOGLEVEL = LOGLEVEL.LEVEL_NOTSET

def get_logging_level() -> LOGLEVEL:
    return _curlevel


def set_new_logging_level(level: LOGLEVEL) -> None:
    global _isdebug, _curlevel
    _curlevel = level
    if level == LOGLEVEL.LEVEL_DEBUG:
        _isdebug = True
    elif level == LOGLEVEL.LEVEL_VERBOSE:
        level = LOGLEVEL.LEVEL_DEBUG
    applog.setLevel(int(level.value))


def initlog(level: LOGLEVEL=LOGLEVEL.LEVEL_INFO) -> None:    
    # formatter = '%(asctime)s - %(name)s[%(levelname).1s] - %(message)s'
    # formatter = '%(name)s[%(levelname).1s] - %(message)s'
    formatter = '[%(levelname).1s] %(message)s'

    logging.basicConfig(format=formatter, datefmt="%b%d %H:%M:%S") # level=logging.NOTSET,
    set_new_logging_level(level)


def isDebug():
    return _isdebug

def infolog(*msg) -> None:
    applog.info(*msg)

def errorlog(*msg) -> None:
    applog.error(*msg)

def debuglog(*msg) -> None:
    applog.debug(*msg)

def warnlog(*msg) -> None:
    applog.warning(*msg)

def verboselog(*msg) -> None:
    if _curlevel == LOGLEVEL.LEVEL_VERBOSE:
        applog.debug(*msg)
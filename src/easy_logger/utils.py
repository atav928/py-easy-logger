# pylint: disable=too-many-arguments
"""Utilities and Decorators."""

from functools import partial
import time
import random

from pathlib import Path
import platform
import tempfile

from easy_logger import reformat_exception, decorator

def set_bool(value: str, default: bool = False):
    """sets bool value when pulling string from os env

    Args:
        value (str|bool, Required): the value to evaluate
        default (bool): default return bool value. Default False

    Returns:
        (str|bool): String if certificate path is passed otherwise True|False
    """
    value_bool = default
    if isinstance(value, bool):
        value_bool = value
    elif str(value).lower() == 'true':
        value_bool = True
    elif str(value).lower() == 'false':
        value_bool = False
    elif Path.exists(Path(value)):
        value_bool = value
    return value_bool


def get_log_dir() -> str:
    """Get default log directory depending on OS.

    :return: Log Directory for System.
    :rtype: str
    """
    directory: dict[str, Path] = {
        "darwin": Path.joinpath(Path.home() / "Library/Logs"),
        "linux": Path("/var/log")
    }
    plat: str = platform.system()
    try:
        return str(directory[plat.lower()])
    except KeyError:
        return tempfile.gettempdir()


def __retry_interval(func, exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1, jitter=0,logger=None):
    """
    Executes a function and retries it if it failed.

    :param func: the funciton to execute.
    :type func: Function
    :param exceptions: an exception or tupple of exceptions to catch, defaults to Exception
    :type exceptions: Exception|tuple[Excpetion,Exception], optional
    :param tries: the maximum number of attempts, defaults to -1 (infinite).
    :type tries: int, optional
    :param delay: intial delay between attempts, defaults to 0.
    :type delay: int, optional
    :param max_delay: the maximum value of delay, defaults to None (no limit).
    :type max_delay: int, optional
    :param backoff: multiplier applied to delay between attempts, defaults to 1 (no backoff).
    :type backoff: int, optional
    :param jitter: extra seconds added to delay between attempts, defaults to 0
                   fixed if a number, random if a tuple (min,max)
    :type jitter: int|tuple[int,int], optional
    :param logger: logger.warning(fmt,error,delay) will be called on failed attempts, defaults to None
                    default is disabled.
    :type logger: Logger, optional
    :return: the result of the func Function.
    """
    _tries, _delay = tries,delay
    while _tries:
        try:
            return func()
        except exceptions as err:
            _tries -= 1
            error = reformat_exception(err)
            if not _tries:
                raise
            if logger is not None:
                logger.warning("msg=\"attempt failed\",error=%s,retrying_in=%ss", error, _delay)
            time.sleep(_delay)
            _delay *= backoff
            if isinstance(jitter,tuple):
                _delay += random.uniform(*jitter)
            else:
                _delay += jitter
            if max_delay is not None:
                _delay = min(_delay, max_delay)

def retry(exceptions=Exception,tries=-1,delay=0,max_delay=None,backoff=1,jitter=0,logger=None):
    """
    Returns a retry decorator.

    :param exceptions: an exception or tupple of exceptions to catch, defaults to Exception
    :type exceptions: Exception|tuple[Excpetion,Exception], optional
    :param tries: the maximum number of attempts, defaults to -1 (infinite).
    :type tries: int, optional
    :param delay: intial delay between attempts, defaults to 0.
    :type delay: int, optional
    :param max_delay: the maximum value of delay, defaults to None (no limit).
    :type max_delay: int, optional
    :param backoff: multiplier applied to delay between attempts, defaults to 1 (no backoff).
    :type backoff: int, optional
    :param jitter: extra seconds added to delay between attempts, defaults to 0
                   fixed if a number, random if a tuple (min,max)
    :type jitter: int|tuple[int,int], optional
    :param logger: logger.warning(fmt,error,delay) will be called on failed attempts, defaults to None
                    default is disabled.
    :type logger: Logger, optional
    :return: a retry decorator.
    :rtype: function
    """
    @decorator
    def retry_decorator(func, *fargs, **fkwargs):
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()
        return __retry_interval(partial(func, *args, **kwargs),exceptions, tries, delay, max_delay, backoff, jitter, logger)
    return retry_decorator

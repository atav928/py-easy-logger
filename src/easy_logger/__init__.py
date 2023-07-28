"""Initializtion of Easy Logger."""
import functools

from easy_logger._version import __version__
from easy_logger.log_config import RotatingLog
from easy_logger.log_format import (splunk_format, splunk_hec_format, reformat_exception)

try:
    from decorator import decorator
except ImportError:
    def decorator(caller):
        """ Turns caller into a decorator.
        Unlike decorator module, function signature is not preserved.

        :param caller: caller(f, *args, **kwargs)
        """
        def decor(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return caller(f, *args, **kwargs)
            return wrapper
        return decor

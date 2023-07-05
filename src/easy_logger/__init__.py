"""Initializtion of Easy Logger."""

from easy_logger._version import __version__
from easy_logger.log_config import RotatingLog
from easy_logger.log_format import (splunk_format, splunk_hec_format)

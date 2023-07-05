# pylint: disable=invalid-name, missing-class-docstring, missing-function-docstring,line-too-long
"""Logger."""

from typing import Any
import logging
import logging.handlers
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

import colorlog

from easy_logger.statics import STREAM_COLORS

LOG_FORMAT = '[%(asctime)s] level=%(levelname)-8s name=%(name)-12s fn=%(filename)s ln=%(lineno)d func=%(funcName)s: %(message)s'
LOG_STREAM_FORMAT = '%(log_color)s[%(asctime)s] %(levelname)-8s: %(message)s'

LOGVALUE = {
    'NOTSET': 0,
    'DEBUG': 10,
    'INFO': 20,
    'WARN': 30,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50,
    'FATAL': 50
}


class LogValue(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    FATAL = 50


@dataclass
class Logger:
    name: str
    logDir: str = ''
    logName: str = 'sample.log'
    maxBytes: int = 5242990
    backupCount: int = 5
    mode: str = 'a'
    level: str = 'INFO'
    stream: bool = True
    setLog: bool = True
    setFile: bool = True
    level_set: dict[str, int] = field(default_factory=lambda: {})


def set_logdir() -> Path:
    """Set default logDir if not provided."""

    return Path.home()


def with_suffix(logName) -> str:
    """Add suffix to logname."""

    return str(Path(logName).with_suffix('.log'))


class RotatingLog:
    """Customized RotatigLogger.

    :return: _description_
    :rtype: _type_
    """

    formatter = logging.Formatter(LOG_FORMAT)
    file_handler = None
    stream_formatter = colorlog.ColoredFormatter(LOG_STREAM_FORMAT, log_colors=STREAM_COLORS)
    stream_handler = None
    logger = None
    _setLog: bool = True
    _setFile: bool = True

    def __init__(self, name: str, logName: str = 'sample.log', logDir=None,
                 maxBytes: int = 5242990, backupCount: int = 5, mode: str = 'a', level: str = 'INFO',
                 stream: bool = True, setLog: bool = True, setFile: bool = True) -> None:
        """Create an instance for each new Rotating Logger."""

        logDir: str = logDir if logDir else str(set_logdir())
        logName = with_suffix(logName)
        self.stream: bool = stream
        self.settings = Logger(name=name, logDir=logDir,
                               logName=logName, maxBytes=maxBytes, backupCount=backupCount,
                               mode=mode, level=level, level_set=LOGVALUE,
                               stream=stream, setLog=self._setLog, setFile=setFile)
        self._setLog = setLog
        self._setFile = setFile
        self._create_logger()

    def _create_logger(self) -> None:
        # ensure logDir exists create it if it does not
        self.createLogDir(logDir=Path(self.settings.logDir))
        # self.formatter = logging.Formatter(LOG_FORMAT)
        self.file_handler = logging.handlers.RotatingFileHandler(
            Path.joinpath(Path(self.settings.logDir) / self.settings.logName),
            mode=self.settings.mode, maxBytes=self.settings.maxBytes,
            backupCount=self.settings.backupCount)
        self.file_handler.setFormatter(self.formatter)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.stream_formatter)

        self.logger = logging.getLogger(self.settings.name).setLevel(self.settings.level)
        if self.settings.setFile:
            self.logger = logging.getLogger(self.settings.name).addHandler(self.file_handler)
        if self.settings.stream:
            self.logger = logging.getLogger(self.settings.name).addHandler(self.stream_handler)

    @property
    def setLog(self) -> bool:
        return self._setLog

    @setLog.setter
    def setLog(self, value: bool) -> None:
        self._setLog = value
        self.settings.setLog = self._setLog

    @property
    def setFile(self) -> bool:
        return self._setFile

    @setFile.setter
    def setFile(self, value: bool) -> None:
        self._setFile = value
        self.settings.setFile = self._setFile

    def getLogger(self, name=None):
        """Get the logger instance

        Args:
            name (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        logger = logging.getLogger(self.settings.name) if not name else self.addLogger(name)
        logger.disabled = not self.settings.setLog
        return logger

    def addLogger(self, name):
        """Adds a new logger instance from the root.

        Args:
            name (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.logger = logging.getLogger(name).setLevel(self.settings.level)
        if self.settings.setFile:
            self.logger = logging.getLogger(name).addHandler(self.file_handler)
        self.logger = logging.getLogger(name).propagate = False
        if self.settings.stream:
            self.logger = logging.getLogger(name).addHandler(self.stream_handler)
        return logging.getLogger(name)

    def createLogDir(self, logDir: Path) -> None:
        """Creates log dir if it doesnot exist

        Args:
            logDir (Path): _description_
        """
        if not Path.exists(logDir):
            Path(logDir).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    sample_logger = RotatingLog(name=__name__, logName="sample_test.log",
                                level="DEBUG", stream=True)
    log = sample_logger.getLogger(name="log_config_second")
    log.info("msg=\"This is an information log\"")
    log.debug("msg=\"This is a debug log\"")
    log.warning("msg=\"This is a warn log\"")
    log.critical("msg=\"This is a critical log\"")
    log.error("msg=\"an error message\"")
    log.debug("msg=\"logger was creted\",dir=%s,file_name=%s",
              sample_logger.settings.logDir, sample_logger.settings.logName)

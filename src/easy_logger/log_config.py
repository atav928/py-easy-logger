# pylint: disable=invalid-name, missing-class-docstring, missing-function-docstring,line-too-long
"""Logger."""

from typing import Any
import logging
import logging.handlers
from pathlib import Path
from dataclasses import dataclass, field

import colorlog

from easy_logger.utils import set_logdir, with_suffix
from easy_logger.statics import STREAM_COLORS

LOG_FORMAT = '[%(asctime)s] level=%(levelname)-8s name=%(name)-12s fn=%(filename)s ln=%(lineno)d func=%(funcName)s: %(message)s'
LOG_STREAM_FORMAT = '%(log_color)s[%(asctime)s] %(levelname)-8s: %(message)s'

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

_levelToName: dict[int, str] = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}
_nameToLevel: dict[str, int] = {
    'CRITICAL': CRITICAL,
    'FATAL': FATAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}

def _checkLevel(level) -> int:
    if isinstance(level, int):
        rv = level
    elif str(level) == level:
        if level not in _nameToLevel:
            raise ValueError("Unknown level: %r" % level)
        rv: int = _nameToLevel[level]
    else:
        raise TypeError("Level not an integer or a valid string: %r" % level)
    return rv


@dataclass
class Logger:
    rootName: str
    logDir: str = ''
    logName: str = 'sample.log'
    maxBytes: int = 5242990
    backupCount: int = 5
    mode: str = 'a'
    level: str = 'INFO'
    levelValue: int = 20
    stream: bool = True
    setLog: bool = True
    setFile: bool = True
    level_set: dict[str, int] = field(default_factory=lambda: {})



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
    _name = None
    _level: str = "NOTSET"
    _levelValue: int = _checkLevel(_level)
    _setLog: bool = True
    _setFile: bool = True

    def __init__(self, name: str, logName: str = 'sample.log', logDir=None,
                 maxBytes: int = 5242990, backupCount: int = 5, mode: str = 'a', level: str = 'INFO',
                 stream: bool = True, setLog: bool = True, setFile: bool = True) -> None:
        """Create an instance for each new Rotating Logger."""
        self._levelValue: int = _checkLevel(level)
        self._level: str = _levelToName[self._levelValue]
        self._name: str = name
        logDir: str = logDir if logDir else set_logdir("home")
        logName = with_suffix(logName)
        self.stream: bool = stream
        self.settings = Logger(rootName=name, logDir=logDir,
                               logName=logName, maxBytes=maxBytes, backupCount=backupCount,
                               mode=mode, level=self._level, levelValue=self._levelValue, level_set=_nameToLevel,
                               stream=stream, setLog=self._setLog, setFile=setFile)
        self._setLog = setLog
        self._setFile = setFile
        self._create_logger()

    def _create_logger(self) -> None:
        # ensure logDir exists create it if it does not
        self.createLogDir(logDir=self.settings.logDir)
        self.file_handler = logging.handlers.RotatingFileHandler(
            Path.joinpath(Path(self.settings.logDir) / self.settings.logName),
            mode=self.settings.mode, maxBytes=self.settings.maxBytes,
            backupCount=self.settings.backupCount)
        self.file_handler.setFormatter(self.formatter)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.stream_formatter)

        self.logger = logging.getLogger(self.settings.rootName).setLevel(self.settings.level)
        if self.settings.setFile:
            self.logger = logging.getLogger(self.settings.rootName).addHandler(self.file_handler)
        if self.settings.stream:
            self.logger = logging.getLogger(self.settings.rootName).addHandler(self.stream_handler)
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def level(self) -> str:
        return self._level
    
    @level.setter
    def level(self, value) -> None:
        self._levelValue = _checkLevel(value)
        self._level = _levelToName[self._levelValue]
        self.settings.level = self._level
        self._levelValue = self.settings.levelValue
    
    @property
    def levelValue(self) -> int:
        return self._levelValue
    
    @levelValue.setter
    def levelValue(self, value) -> None:
        self._levelValue = _checkLevel(value)
        self._level = _levelToName[self._levelValue]
        self.settings.level = self._level
        self._levelValue = self.settings.levelValue

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
        """
        Get the logger instance.

        Args:
            name (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        logger = logging.getLogger(self.settings.rootName) if not name else self.addLogger(name)
        logger.disabled = not self.settings.setLog
        return logger

    def addLogger(self, name: str):
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

    def createLogDir(self, logDir: str) -> None:
        """Creates log dir if it doesnot exist

        Args:
            logDir (Path): _description_
        """
        ldir = Path(logDir)
        if not Path.exists(ldir):
            Path(ldir).mkdir(parents=True, exist_ok=True)


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

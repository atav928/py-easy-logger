"""Utilities."""

from pathlib import Path
import platform
import tempfile

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


def get_log_dir(extend_path: str=None) -> str:
    """
    Get default log directory depending on OS. Extend to application path if path supplied.

    :param extend_path: Extends the system default location; creates a new app directory, defaults to None
    :type extend_path: str, optional
    :return: Log Directory for Logs
    :rtype: str
    """
    directory: dict[str, Path] = {
        "darwin": Path.joinpath(Path.home() / "Library/Logs"),
        "linux": Path("/var/log")
    }
    plat: str = platform.system()
    try:
        if extend_path:
            return f"{str(directory[plat.lower()])}/{extend_path}"
        return str(directory[plat.lower()])
    except KeyError:
        if extend_path:
            return f"{str(tempfile.gettempdir())}/{extend_path}"
        return tempfile.gettempdir()
    
def set_logdir(location: str = "home", extend: str="") -> str:
    """Set default logDir if not provided."""
    if location.lower() == "home":
        return get_log_home()
    if location.lower() == "default":
        return get_log_dir()
    if location.lower() == "extend":
        return get_log_dir(extend_path=extend)
    raise ValueError(f"Unknown location type {location}")

def get_log_home() -> str:
    """Return current users `home` direcotry."""
    return str(Path.home())

def with_suffix(logName) -> str:
    """Add suffix to logname."""

    return str(Path(logName).with_suffix('.log'))

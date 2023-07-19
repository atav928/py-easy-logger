"""Utilities"""

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

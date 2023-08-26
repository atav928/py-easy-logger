"""Static."""

ENCODING: str = "utf-8"
BASE_STREAM_COLORS: dict[str, str] = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'bold_red',
    'CRITICAL': 'purple'
}

DEFAULT_STREAM_COLORS: dict[str,str] = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red'    
}

DARK_STREAM_COLORS: dict[str,str] = {
    'DEBUG': 'bold_black',
    'INFO': 'bold_white',
    'WARNING': 'bold_light_black',
    'ERROR': 'bg_light_black',
    'CRITICAL': 'bg_bold_black'    
}

BRIGHT_STREAM_COLORS: dict[str,str] = {
    'DEBUG': 'bg_69',
    'INFO': 'bg_82',
    'WARNING': 'bg_148',
    'ERROR': 'bg_88',
    'CRITICAL': 'bg_89'    
}

COLOR_CODES: dict[str, dict[str, str]] = {
    "BASE_STREAM_COLORS": BASE_STREAM_COLORS,
    "DEFAULT_STREAM_COLORS": DEFAULT_STREAM_COLORS,
    "DARK_STREAM_COLORS": DARK_STREAM_COLORS,
    "BRIGHT_STREAM_COLORS": BRIGHT_STREAM_COLORS
}

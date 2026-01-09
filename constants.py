"""Constants for the Notepad application."""

from enum import IntEnum


class EncodingType(IntEnum):
    """File encoding types."""
    UTF8 = 0
    UTF8_BOM = 1
    UTF16_BE = 2
    UTF16_LE = 3
    WINDOWS_1251 = 4
    OEM_866 = 5


class LineEnding(IntEnum):
    """Line ending types."""
    WINDOWS_CRLF = 0
    UNIX_LF = 1


class TextFormat(IntEnum):
    """Text format types."""
    TEXT_FILE = 0
    OTHER = 1


# Encoding mappings
ENCODING_NAMES = {
    EncodingType.UTF8: "UTF-8",
    EncodingType.UTF8_BOM: "UTF-8 BOM",
    EncodingType.UTF16_BE: "UTF-16 BE BOM",
    EncodingType.UTF16_LE: "UTF-16 LE BOM",
    EncodingType.WINDOWS_1251: "Windows 1251",
    EncodingType.OEM_866: "OEM 866",
}

ENCODING_PYTHON_NAMES = {
    EncodingType.UTF8: "utf_8",
    EncodingType.UTF8_BOM: "utf_8_sig",
    EncodingType.UTF16_BE: "utf_16_be",
    EncodingType.UTF16_LE: "utf_16_le",
    EncodingType.WINDOWS_1251: "cp1251",
    EncodingType.OEM_866: "cp866",
}

# Line ending strings
LINE_ENDING_STRINGS = {
    LineEnding.WINDOWS_CRLF: "\r\n",
    LineEnding.UNIX_LF: "\n",
}

# Default values
DEFAULT_FONT_FAMILY = "Segoe UI"
DEFAULT_FONT_SIZE = 12
DEFAULT_FONT_WEIGHT = 500
DEFAULT_FONT_ITALIC = False
DEFAULT_ZOOM_INCREMENT = 1
MIN_ZOOM_LEVEL = -6
TAB_STOP_SPACES = 4

# Color defaults
DEFAULT_TEXT_COLOR = "#000000"
DEFAULT_BACKGROUND_COLOR = "#ffffff"
DEFAULT_LINE_COLOR = "#e8e8ff"
DEFAULT_LINE_NUMBER_AREA_TEXT = "#000000"
DEFAULT_LINE_NUMBER_AREA_BACKGROUND = "#c0c0c0"

# UI defaults
DEFAULT_STYLE = "windowsvista"
DEFAULT_LANGUAGE = "English"
DEFAULT_MAX_RECENT_FILES = 5
DEFAULT_ICON_SIZE = 24

# File extensions
TEXT_FILE_EXTENSIONS = ("txt", "TXT")

# Application version
APP_VERSION = "0.1.2"
APP_RELEASE_DATE = "2026/01/09"
APP_DEVELOPER = "Yuri Pavlov"
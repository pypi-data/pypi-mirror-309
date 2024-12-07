# ----------------------------------------------------------------------
# |  Object Tools
# ----------------------------------------------------------------------
from .enumeration import Key, Value
from .exceptions import (
    CacheError,
    ConsoleError,
    DirectoryError,
    FileSystemError,
    KeyValueError,
    JSONError,
    RangeError,
    SettingsError,
    TimeError,
    TyperAppError,
    UserOptionsError,
    UserSettingsError,
)
from .pickling import pdumps, ploads
from .singleton import singleton_decorator as singleton


__version__ = "v1.0.0"


__all__ = [
    "Key",
    "Value",
    "CacheError",
    "ConsoleError",
    "DirectoryError",
    "FileSystemError",
    "KeyValueError",
    "JSONError",
    "RangeError",
    "SettingsError",
    "TimeError",
    "TyperAppError",
    "UserOptionsError",
    "UserSettingsError",
    "pdumps",
    "ploads",
    "singleton",
    "__version__",
]

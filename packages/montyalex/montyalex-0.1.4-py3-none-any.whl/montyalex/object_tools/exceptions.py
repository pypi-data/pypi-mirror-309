# ----------------------------------------------------------------------
# |  Exceptions
# ----------------------------------------------------------------------
from json import JSONDecodeError
from montyalex.typing_tools import Any


# ----------------------------------------------------------------------
# |  Base Exceptions
# ----------------------------------------------------------------------
class MontyBaseException(BaseException):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "MontyBaseException",
    ) -> None:
        super().__init__(message)
        self.name = name
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f"{self.name}: {self.message} {self.value}"

    def __repr__(self) -> str:
        return self.name

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class MontyArithmeticException(ArithmeticError):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "MontyArithmeticException",
    ) -> None:
        super().__init__(message)
        self.name = name
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f"{self.name}: {self.message} {self.value}"

    def __repr__(self) -> str:
        return self.name

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class MontyJSONException(JSONDecodeError):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "MontyJSONException",
    ) -> None:
        super().__init__(message, "", 0)
        self.name = name
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f"{self.name}: {self.message} {self.value}"

    def __repr__(self) -> str:
        return self.name

    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return self.__class__, (self.message, self.value)


class MontyAlexException(MontyBaseException):
    def __init__(
        self, message: str, value: Any, name: str = "MontyAlexException"
    ) -> None:
        super().__init__(message, value, name)


class MontyAppException(MontyAlexException):
    def __init__(
        self, message: str, value: Any, name: str = "MontyAppException"
    ) -> None:
        super().__init__(message, value, name)


class MontyTyperException(MontyBaseException):
    def __init__(
        self,
        message: str,
        value: Any,
        name: str = "MontyTyperException",
    ) -> None:
        super().__init__(message, value, name)


class MontyOSException(MontyAppException):
    def __init__(
        self, message: str, value: Any, name: str = "MontyOSException"
    ) -> None:
        super().__init__(message, value, name)


class MontyUserException(MontyAppException):
    def __init__(
        self, message: str, value: Any, name: str = "MontyUserException"
    ) -> None:
        super().__init__(message, value, name)


# ----------------------------------------------------------------------
# |  Custom Errors
# ----------------------------------------------------------------------
class SettingsError(MontyAppException):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "SettingsError",
    ) -> None:
        super().__init__(message, value, name)


class TyperAppError(MontyTyperException):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "TyperAppError",
    ) -> None:
        super().__init__(message, value, name)


class CacheError(MontyAppException):
    def __init__(
        self, message: str, value: Any = None, name: str = "CacheError"
    ) -> None:
        super().__init__(message, value, name)


class ConsoleError(MontyAppException):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "ConsoleError",
    ) -> None:
        super().__init__(message, value, name)


class DirectoryError(MontyOSException):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "DirectoryError",
    ) -> None:
        super().__init__(message, value, name)


class FileSystemError(MontyOSException):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "FileSystemError",
    ) -> None:
        super().__init__(message, value, name)


class TimeError(MontyAppException):
    def __init__(
        self, message: str, value: Any = None, name: str = "TimeError"
    ) -> None:
        super().__init__(message, value, name)


class UserOptionsError(MontyUserException):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "UserOptionsError",
    ) -> None:
        super().__init__(message, value, name)


class UserSettingsError(MontyUserException):
    def __init__(
        self,
        message: str,
        value: Any = None,
        name: str = "UserSettingsError",
    ) -> None:
        super().__init__(message, value, name)


class RangeError(MontyArithmeticException):
    def __init__(
        self, message: str, value: Any = None, name: str = "RangeError"
    ) -> None:
        super().__init__(message, value, name)


class KeyValueError(MontyBaseException):
    def __init__(
        self, message: str, value: Any = None, name: str = "RangeError"
    ) -> None:
        super().__init__(message, value, name)


class JSONError(MontyJSONException):
    def __init__(
        self, message: str, value: Any = None, name: str = "JSONError"
    ) -> None:
        super().__init__(message, value, name)

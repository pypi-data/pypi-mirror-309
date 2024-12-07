# ----------------------------------------------------------------------
# |  Path
# ----------------------------------------------------------------------
from pathlib import Path


def current_path(path=".") -> Path:
    """Returns the current path"""
    return Path(path)


def current_working_path(path: Path) -> Path:
    """Returns the current working directory path"""
    return current_path(path).resolve()


# ----------------------------------------------------------------------
# |  Appending paths
# ----------------------------------------------------------------------
def appendp(
    path: str, *others: str, current_directory: bool = False
) -> Path:
    """Append paths to another path"""
    _path = current_path(path).joinpath(*map(str, others))
    return current_working_path(_path) if current_directory else _path


def appendf(
    path: str,
    *others: str,
    filename: str,
    suffix: str = None,
    current_directory: bool = False,
) -> Path:
    """Append a filename to a path, with an optional suffix."""
    return appendp(
        path,
        *others,
        f"{filename}.{suffix}" if suffix else filename,
        current_directory=current_directory,
    )


def isabsolute(path: str) -> bool:
    """Returns True if the path is absolute, False otherwise."""
    return Path(path).is_absolute()


def isrelative(path: str) -> bool:
    """Returns True if the path is relative, False otherwise."""
    return not isabsolute(path)


def isfile(path: str) -> bool:
    """
    Returns True if the path refers to a regular file (not a directory).
    """
    return Path(path).is_file()


def readfile(path: str) -> str:
    """
    Reads the contents of a file at the given path, decoding with UTF-8.
    """
    return Path(path).read_text(encoding="UTF-8")


def pathexists(path: str, debug_cwd: bool = False) -> bool:
    """
    Returns True if the path refers to an existing path.
    If debug_cwd is True, prints the absolute path.
    """
    if debug_cwd:
        path = current_working_path(path)
        print(path)
    abs = isabsolute(path)
    return Path(path).exists() if abs else False


# ----------------------------------------------------------------------
# |  Example Usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    for _ in range(100):
        appended = appendf(
            "src",
            "montyalex",
            "fs_tools",
            f"{_:02}",
            filename="paths",
            suffix="py",
            current_directory=True,
        )
        E = pathexists(appended)
        absolute = isabsolute(appended)
        relative = isrelative(appended)
        print(appended, E, absolute, relative)

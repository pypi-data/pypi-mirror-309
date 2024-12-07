# ----------------------------------------------------------------------
# |  Simple-Directories
# ----------------------------------------------------------------------
from montyalex.console_tools import richconsole, success_stm
from montyalex.fs_tools import (
    current_working_dir as cwd,
    joinpaths,
    mkdirs,
    pathexists,
)
from .helpdirs import remove_formatted__dir

print = richconsole.print


def create_simple_directories(
    range_: int = 1,
    name_: str = None,
    prefix: str = None,
    suffix: str = None,
    silent: bool = False,
):
    for i in range(range_):
        formatted = name_ if name_ else f"{i:03}"
        if prefix:
            formatted = f"{prefix}{formatted}"
        if suffix:
            formatted = f"{formatted}{suffix}"
        mkdirs(joinpaths(cwd, formatted), exist_ok=True)
        if not silent:
            print(f"{success_stm}, Created {formatted!r} in {cwd!r}")


def remove_simple_directories(
    range_: int = 1,
    name_: str = None,
    prefix: str = None,
    suffix: str = None,
    silent: bool = False,
):
    for i in range(range_):
        formatted = name_ if name_ else f"{i:03}"
        if prefix:
            formatted = f"{prefix}{formatted}"
        if suffix:
            formatted = f"{formatted}{suffix}"
        formatted_directory = joinpaths(cwd, formatted)
        remove_formatted__dir(formatted_directory, silent)

        if not pathexists(formatted_directory) and not silent:
            print(f"{success_stm}, Removed {formatted!r} from {cwd!r}")

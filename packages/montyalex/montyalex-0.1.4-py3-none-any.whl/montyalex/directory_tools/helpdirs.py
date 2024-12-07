# ----------------------------------------------------------------------
# |  Help-Directories
# ----------------------------------------------------------------------
import shutil

from montyalex.console_tools import richconsole, error_stm
from montyalex.fs_tools import pathexists

print = richconsole.print


def remove_formatted__dir(
    dir: str | bytes, silent: bool = False
) -> bool:
    if pathexists(dir):
        try:
            shutil.rmtree(dir)
            return True
        except (OSError, NotADirectoryError, IsADirectoryError):
            if not silent:
                print(
                    f"{error_stm}, Removing {dir!r} failed in the directory given"
                )
            return False
    else:
        if not silent:
            print(
                f"Warning, Attempted to remove {dir!r}, "
                + "but it didn't exist"
            )
        return False

# ----------------------------------------------------------------------
# |  Paths
# ----------------------------------------------------------------------
import os
from posixpath import abspath, expanduser
import shutil
from pathlib import Path


# ----------------------------------------------------------------------
# |  Global shorthand for os, path, and file system functions
# ----------------------------------------------------------------------
joinpaths: callable = os.path.join
pathexists: callable = os.path.exists
_: callable = abspath, expanduser
current_working_dir: str = os.getcwd()
current_working_path: str = Path().cwd()


def rmfile(
    path,
):
    os.remove(path=path)


def mkdirs(name, mode: int = 511, exist_ok: bool = False):
    os.makedirs(name=name, mode=mode, exist_ok=exist_ok)


def rmdirs(
    name,
):
    os.removedirs(name=name)


def rmtree(
    path,
):
    shutil.rmtree(path=path)

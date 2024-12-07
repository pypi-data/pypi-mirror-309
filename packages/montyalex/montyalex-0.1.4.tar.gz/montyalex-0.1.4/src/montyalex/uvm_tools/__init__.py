# ----------------------------------------------------------------------
# |  User-Virtual-Memory Tools
# ----------------------------------------------------------------------
import os
import psutil
from .virmem_process import VirMemProcess


# ----------------------------------------------------------------------
# |  Global Virtual Memory Process Object
# ----------------------------------------------------------------------
vmprocess = VirMemProcess()

__version__ = "v1.0.0"


__all__ = ["vmprocess", "__version__"]

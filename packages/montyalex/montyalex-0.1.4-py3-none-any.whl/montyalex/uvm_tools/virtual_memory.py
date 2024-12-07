# ----------------------------------------------------------------------
# |  Virtual Memory
# ----------------------------------------------------------------------
import os
import psutil
from .memory_utils import virtualmem


class VirtualMemory:
    """
    VirtualMemory management

    Attrs:
        system (dict): A dict containing total, available, used, and recommended maximum memory.
        pid (int): The process ID of the current Python process.
        process (psutil.Process): The current Python process.
        memory_info (psutil.Process.memory_info): The memory info of the current Python process.
        used (float): The used memory of the current Python process in MB.
        rss (float): The resident set size of the current Python process in MB.

    Methods:
        __call__: Updates the system memory and RSS values.
        __float__: Returns the recommended maximum memory in MB.
    """

    def __init__(self) -> None:
        self.system = virtualmem()
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)
        self.memory_info = self.process.memory_info()
        self.used = self.system["used"]
        self.rss = self.memory_info.rss / (1024**2) - self.used

    def __float__(self) -> float:
        return self.system["recommended_maximum"]

    def __call__(self) -> "VirtualMemory":
        self.system = virtualmem()
        self.memory_info = self.process.memory_info()
        self.rss = self.memory_info.rss / (1024**2) - self.used
        return self

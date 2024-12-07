# ----------------------------------------------------------------------
# |  Virtual Memory Process
# ----------------------------------------------------------------------
from .virtual_memory import VirtualMemory


class VirMemProcess:
    """
    Management for virtual memory processes with context capabilities

    Attrs:
        available (bool): Flag to set recommended_maximum to available memory.
        double (bool): Flag to double the recommended_maximum.
        maximum (bool): Flag to set recommended_maximum to total system memory.
        usage (bool): Flag to print memory usage details.
        virmem (VirtualMemory): An instance of the VirtualMemory class.
        system (dict): The system memory details from the VirtualMemory instance.

    Methods:
        __call__: Updates the flags for managing memory.
        __enter__: Context manager entry, configures memory settings based on flags.
        __exit__: Context manager exit, cleans up resources.
    """

    def __init__(self) -> None:
        self.available: bool = False
        self.double: bool = False
        self.maximum: bool = False
        self.usage: bool = False
        self.virmem = VirtualMemory()
        self.system = self.virmem.system

    def __call__(
        self,
        *,
        available: bool = False,
        double: bool = False,
        maximum: bool = False,
        usage: bool = False,
    ) -> None:
        self.available: bool = available
        self.double: bool = double
        self.maximum: bool = maximum
        self.usage: bool = usage
        self.virmem = VirtualMemory()
        return self

    def __enter__(self):
        self.virmem()

        if self.available:
            self.system["recommended_maximum"] = self.system[
                "available"
            ]
        if self.double:
            self.system["recommended_maximum"] *= 2
        if self.maximum:
            self.system["recommended_maximum"] = self.system["total"]
        if self.usage:
            print(f'System Used: {self.system["used"]:.2f}gb')
            print(f'System Available: {self.system["available"]:.2f}gb')
            print(f'System Total: {self.system["total"]:.2f}gb')
            print(
                f'Recommended Maximum: {self.system["recommended_maximum"]:.2f}gb'
            )
            print(f"Process Used: {self.virmem.rss / 2:.2f}gb")
        if float(self.virmem) > self.virmem.rss / 2:
            return self
        raise MemoryError(
            "Context manager not allowed due to insufficient available memory"
        )

    def __exit__(self, type, value, traceback):
        pass

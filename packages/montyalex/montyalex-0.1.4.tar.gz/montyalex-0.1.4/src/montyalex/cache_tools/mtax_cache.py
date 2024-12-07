# ----------------------------------------------------------------------
# |  MontyAlex Cache
# ----------------------------------------------------------------------
import platform
from diskcache import Cache
import psutil

from montyalex.console_tools import richconsole, success_stm
from montyalex.fs_tools import (
    current_working_dir,
    joinpaths,
    pathexists,
)
from montyalex.time_tools import MtaxTime
from montyalex.typing_tools import NoneType
from .cache_helpers import remove_cache__dir

print = richconsole.print


DIR = joinpaths(".mtax", "cache")
mtax: Cache = Cache(DIR)
os_name = platform.system()
os_strength = platform.processor()
py_ver = platform.python_version()
cache_exists = joinpaths(current_working_dir, DIR, "cache.db")

svmem = psutil.virtual_memory()

total_ram_bytes = svmem.total
total_ram_gb = total_ram_bytes / (1024**3)

available_ram_bytes = svmem.available
available_ram_gb = available_ram_bytes / (1024**3)

used_ram_bytes = total_ram_bytes - available_ram_bytes
used_ram_gb = used_ram_bytes / (1024**3)


def style(
    s: str,
    *,
    color: str = "default",
    bold: bool = False,
    indent: int = 4,
) -> str:
    styled = f"[{color}]{s}[/]"
    if bold:
        styled = f"[bold]{styled}[/]"
    indented_styled = f'{" " * indent}{styled}'
    return indented_styled


class MtaxCache:
    """
    A class to manage a disk cache.

    The cache is stored in a SQLite database in the current working
    directory. The cache is keyed by strings, and the values are any
    Python object that can be pickled.

    The cache also stores some information about the current Python
    interpreter, such as the version, the operating system, and the
    amount of available RAM.

    The cache can be cleared, and individual items can be removed.

    The cache can be listed, showing all the key-value pairs.

    The cache can be reset, which clears the cache and sets the
    Python interpreter information to the current values.

    The cache can be checked, which shows information about the
    current Python interpreter, and checks if the cache directory
    exists.
    """

    def __init__(self, timezone: str = "Etc/Greenwich") -> None:
        self.cache = mtax
        self.status: str = "Ok"
        self.os_ = os_name
        self.os_strength = os_strength
        self.py_ver = py_ver
        self.total_ram_gb = total_ram_gb
        self.available_ram_gb = available_ram_gb
        self.used_ram_gb = used_ram_gb
        self.datetime: MtaxTime = MtaxTime(timezone)

    def add_item(self, item: tuple[str, str], silent: bool = False):
        if not silent:
            print(f"Adding {item[0]!r} to Cache")
        self.cache.add("_timestamp_", self.datetime.timestamp())
        self.cache.add(item[0], item[1])
        if not silent:
            print(f"{success_stm}, Added {item[0]!r} to Cache")

    def set_item(self, item: tuple[str, str], silent: bool = False):
        to_message = f"{item[0]!r} to {item[1]!r}"
        if not silent:
            print(f"Setting {to_message} in the Cache")
        self.cache.set("_timestamp_", self.datetime.timestamp())
        self.cache.set(item[0], item[1])
        print(f"{success_stm}, Set {to_message} in the Cache")

    def get_item(self, key: str, silent: bool = False):
        if not silent:
            print(f"Getting {key!r} from the Cache")
        item_value = self.cache.get(key)
        if not silent:
            print(f"{success_stm}, Got {key!r} from the Cache")
            print(
                f"The value for {key!r} in the Cache is {item_value!r}"
            )
        if not silent:
            print(f"{key!r}={item_value!r}")
        return item_value

    def incr_item(self, key: str, silent: bool = False):
        if not silent:
            print(f"Incrementing {key!r} in the Cache")
        value = self.cache.incr(key)
        value = max(value, 0)
        if not silent:
            print(
                f"{success_stm}, Incremented {key!r}"
                f" in the Cache to {value}"
            )
        return value

    def decr_item(self, key: str, silent: bool = False):
        if not silent:
            print(f"Decrementing {key!r} in the Cache")
        value = self.cache.decr(key)
        value = max(value, 0)
        if not silent:
            print(
                f"{success_stm}, Decremented {key!r}"
                f" in the Cache to {value}"
            )
        return value

    def clear(self, silent: bool = False):
        if not silent:
            print("Clearing Cache")
        self.cache.clear()
        remove_cache__dir(DIR, silent)
        if not silent:
            print("Cache Cleared")

    def reset(self, silent: bool = False):
        if not silent:
            print("Resetting Cache")
        self.remove("_python_", silent)
        self.remove("_datedirs_", silent)
        self.remove("_cache-tools_", silent)
        self.remove("_directory-tools_", silent)
        self.add_item(
            ("_python_", f"v{platform.python_version()}"), silent
        )
        self.add_item(("_datedirs_", "v1.0.0"), silent)
        self.add_item(("_cache-tools_", "v1.0.0"), silent)
        self.add_item(("_directory-tools_", "v1.0.0"), silent)
        if not silent:
            print("Cache Reset")

    def remove(self, key: str, silent: bool = False):
        if not silent:
            print(f"Removing {key!r}")
        self.cache.delete(key)
        if not silent:
            print(f"{success_stm}, Removed {key!r} from Cache")

    def list_k_v_pairs(self, silent: bool = False):
        cached_items = list(self.cache)
        cached_items.sort()
        for key in cached_items:
            value = self.cache.get(key)
            print(f"[bold]{key}[/]: {value!r}")
        if not silent:
            ...

    def info(self, list_: bool = False, silent: bool = False):
        current_time = f"{self.datetime.timestamp()!r}"
        current_status = f"{self.status!r}"
        current_strength = f"{self.os_strength!r}"
        current_os = f"{self.os_!r}"

        current_py_ver = f"[yellow]'v{self.py_ver}'[/]"

        current_aram = f"[sky_blue2]{self.available_ram_gb:.2f}GB[/]"
        none_aram = f"[orange4]{0:.2f}GB [bold]???[/][/] NONE FOUND"

        current_uram = f"[deep_pink3]{self.used_ram_gb:.2f}GB[/]"
        none_uram = f"[green1]{0:.2f}GB [bold]???[/][/] NONE FOUND"

        current_tram = f"[sky_blue2]{self.total_ram_gb:.2f}GB[/]"
        none_tram = f"[orange4]{0:.2f}GB [bold]???[/][/] NONE FOUND"
        print(f"{style('Info', bold=True)}: [")
        print(
            style(
                f"{style(
                    'Current',
                    bold=True)}: {current_time}",
                indent=2,
            )
        )
        if self.status == "Ok":
            print(
                style(
                    f"{style(
                        'Status',
                        bold=True)}: [green]{current_status}[/]",
                    indent=2,
                )
            )
        else:
            print(
                style(
                    f"{style(
                        'Status',
                        bold=True)}: [red]{current_status}[/]",
                    indent=2,
                )
            )
        print(
            style(
                f"{style(
                    'System Processor',
                    bold=True)}: {current_strength}",
                indent=2,
            )
        )
        print(
            style(
                f"{style(
                    'Operating System',
                    bold=True)}: {current_os}",
                indent=2,
            )
        )
        if self.os_strength and self.os_:
            print(
                style(
                    f"{style(
                        'Python Version',
                        bold=True)}: {current_py_ver}",
                    indent=4,
                )
            )
            if self.available_ram_gb:
                print(
                    style(
                        f"{style(
                            'RAM Available',
                            bold=True)}: {current_aram}",
                        indent=4,
                    )
                )
            else:
                print(
                    style(
                        f"{style(
                            'RAM Available',
                            bold=True)}: {none_aram}",
                        indent=4,
                    )
                )
            if self.used_ram_gb:
                print(
                    style(
                        f"{style(
                            'RAM Used',
                            bold=True)}: {current_uram}",
                        indent=4,
                    )
                )
            else:
                print(
                    style(
                        f"{style(
                            'RAM Used',
                            bold=True)}: {none_uram}",
                        indent=4,
                    )
                )
            if self.total_ram_gb > 0:
                print(style(f"RAM Total: {current_tram}", indent=4))
            else:
                print(style(f"RAM Total: {none_tram}", indent=4))
            print(style("Status: [green]'Good'[/]", indent=4))
        else:
            print(style("Status: [red]'Bad'[/]", indent=4))
        if pathexists(cache_exists):
            print(
                style(
                    f"{style(
                        'Cache Directory',
                        bold=True)}: [green]{DIR!r}[/]",
                    indent=2,
                )
            )
            print(
                style(
                    f"{style(
                        'File',
                        bold=True)}: [green]'cache.db'[/]",
                    indent=4,
                )
            )
        else:
            print(
                style(
                    f"{style(
                    'Cache Directory',
                    bold=True)}: [red]{DIR!r}[/]",
                    indent=2,
                )
            )
            print(
                style(
                    f"{style(
                        'File',
                        bold=True)}: [red]'cache.db'[/] [dim](does not exist)[/]",
                    indent=4,
                )
            )
        py_ver_cached = self.get_item("_python_", True)
        cat_ver_cached = self.get_item("_cache-tools_", True)
        cot_ver_cached = self.get_item("_console-tools_", True)
        dir_ver_cached = self.get_item("_directory-tools_", True)
        if isinstance(py_ver_cached, NoneType):
            print(
                style(
                    f"{style(
                    'Python Version',
                    bold=True)}: {py_ver_cached!r}",
                    indent=4,
                )
            )
        else:
            print(
                style(
                    f"{style(
                    'Python Version',
                    bold=True)}: [yellow]{py_ver_cached!r}[/]",
                    indent=4,
                )
            )
        if isinstance(cat_ver_cached, NoneType):
            print(
                style(
                    f"{style(
                    'CacheTools Version',
                    bold=True)}: {cat_ver_cached!r}",
                    indent=4,
                )
            )
        else:
            print(
                style(
                    f"{style(
                    'CacheTools Version',
                    bold=True)}: [cyan2]{cat_ver_cached!r}[/]",
                    indent=4,
                )
            )
        if isinstance(cot_ver_cached, NoneType):
            print(
                style(
                    f"{style(
                    'ConsoleTools Version',
                    bold=True)}: {cot_ver_cached!r}",
                    indent=4,
                )
            )
        else:
            print(
                style(
                    f"{style(
                    'ConsoleTools Version',
                    bold=True)}: [cyan2]{cot_ver_cached!r}[/]",
                    indent=4,
                )
            )
        if isinstance(dir_ver_cached, NoneType):
            print(
                style(
                    f"{style(
                    'DirectoryTools Version',
                    bold=True)}: {dir_ver_cached!r}",
                    indent=4,
                )
            )
        else:
            print(
                style(
                    f"{style(
                    'DirectoryTools Version',
                    bold=True)}: [cyan2]{dir_ver_cached!r}[/]",
                    indent=4,
                )
            )
        if list_:
            print("]..,")
            self.list_k_v_pairs()
        else:
            print("]")
        if not silent:
            ...

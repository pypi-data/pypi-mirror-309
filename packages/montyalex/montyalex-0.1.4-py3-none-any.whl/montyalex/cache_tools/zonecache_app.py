# ----------------------------------------------------------------------
# |  (Time)Zone-Cache App
# ----------------------------------------------------------------------
from montyalex.time_tools import MtaxTime
from montyalex.typer_tools import Option, Typer
from .mtax_cache import MtaxCache


# ----------------------------------------------------------------------
# |  Typer App
# ----------------------------------------------------------------------
zone_: Typer = Typer(
    name="zone", help="Manage timezone-data in the cache"
)


# ----------------------------------------------------------------------
# |  Typer Commands; reset_, set_, get_
# ----------------------------------------------------------------------
@zone_.command(name="reset")
def reset_(
    *,
    timezone: str = "Etc/Greenwich",
    silent: bool = Option(
        False,
        "-s",
        show_default="-!s",
        help="Silence extraneous messages in console",
    ),
):
    """Reset timezone in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax_time = MtaxTime(timezone)
    mtax.remove("_timezone_", silent)
    set_(timezone=mtax_time.timezone, silent=silent)


@zone_.command(name="set")
def set_(
    *,
    timezone: str = "Etc/Greenwich",
    silent: bool = Option(
        False,
        "-s",
        show_default="-!s",
        help="Silence extraneous messages in console",
    ),
):
    """Set timezone in the cache"""
    mtax: MtaxCache = MtaxCache(timezone)
    mtax_time = MtaxTime(timezone)
    mtax.set_item(("_timezone_", mtax_time.timezone), silent)


@zone_.command(name="get")
def get_(
    *,
    silent: bool = Option(
        False,
        "-s",
        show_default="-!s",
        help="Silence extraneous messages in console",
    ),
):
    """Set timezone in the cache"""
    mtax: MtaxCache = MtaxCache("Etc/Greenwich")
    mtax.get_item("_timezone_", silent)

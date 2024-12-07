# ----------------------------------------------------------------------
# |  Cache Tools
# ----------------------------------------------------------------------
from .mtax_cache import MtaxCache
from .cache_app import (
    cache_,
    get_ as get_cache_item,
    add_ as add_cache_item,
    set_ as set_cache_item,
    incr_ as incr_cache_item,
    decr_ as decr_cache_item,
    remove_ as remove_cache_item,
    info_ as cache_info,
    list_ as cache_list,
    clear_ as cache_clear,
    reset_ as cache_reset)


__version__ = 'v1.0.0'


__all__ = [
    "MtaxCache",
    "cache_",
    "get_cache_item",
    "add_cache_item",
    "set_cache_item",
    "incr_cache_item",
    "decr_cache_item",
    "remove_cache_item",
    "cache_info",
    "cache_list",
    "cache_clear",
    "cache_reset",
    "__version__"]

# ----------------------------------------------------------------------
# |  Memory Utilities
# ----------------------------------------------------------------------
import psutil


# ----------------------------------------------------------------------
# |  User Memory Dictionary
# ----------------------------------------------------------------------
def virtualmem() -> dict[str, float]:
    """
    Returns a dictionary containing the total, recommended maximum, available,
    and used memory in gigabytes.
    """
    total = psutil.virtual_memory().total / (1024**3)
    available = psutil.virtual_memory().available / (1024**3)
    used = psutil.virtual_memory().used / (1024**3)
    recommended_maximum = total / 4

    return {
        "total": total,
        "recommended_maximum": recommended_maximum,
        "available": available,
        "used": used,
    }

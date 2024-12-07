from montyalex.fs_tools import cancel


def date_directories(
    name_: str, prefix: str, suffix: str, silent: bool = False
):
    if (name_ or prefix or suffix) and not silent:
        print("Not allowed with the -datedirs option")
        cancel()

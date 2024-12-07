# ----------------------------------------------------------------------
# |  MontyAlex App
# ----------------------------------------------------------------------
from ._mtax import save_mtax_commands
from ._settings import settings_
from .cache_tools import cache_, incr_cache_item, decr_cache_item

from .console_tools import richconsole
from .directory_tools import (
    datedirs,
    rmdatedirs,
    simpledirs,
    rmsimpledirs,
)
from .time_tools import func_time
from .typer_helpers import (
    blueprints_help,
    commands_help,
    date_directories,
    funcargs_help,
)
from .typer_tools import Option, Typer

print = richconsole.print


# ----------------------------------------------------------------------
# |  Typer App
# ----------------------------------------------------------------------
monty: Typer = Typer(
    name="monty",
    add_help_option=False,
    pretty_exceptions_show_locals=False,
)
monty.add_typer(settings_)
monty.add_typer(cache_)
LINEDASH = f'{"_" * 80}'


# ----------------------------------------------------------------------
# |  Typer Commands; create__dirs (mk), remove__dirs (rm), mtax
# ----------------------------------------------------------------------
@monty.command(name="mk")
@func_time("to create the directories")
def create__dirs(
    range_: int = Option(1, "--range", "-r"),
    s_dirs: bool = Option(
        False,
        "--simple-directories",
        "-dirs",
        is_flag=True,
        show_default="range: 1",
    ),
    dt_dirs: bool = Option(
        False,
        "--date-directories",
        "-datedirs",
        is_flag=True,
        show_default="range: 1yr",
    ),
    four_weeks: bool = Option(
        False, "--four-weeks", "-4w", is_flag=True
    ),
    dir_parent: str = Option(None, "--parent", "-p"),
    dir_name: str = Option(None, "--name"),
    prefix: str = Option(None, "--prefix"),
    suffix: str = Option(None, "--suffix"),
    silent: bool = Option(
        False,
        "-s",
        show_default="-!s",
        help="Silence extraneous messages in console",
    ),
) -> None:
    """
    Creates new folders in the current local directory

    Args:
        range_ (int): The number of directories to create.
        s_dirs (bool): A flag to create simple directories.
        dt_dirs (bool): A flag to create date directories.
        four_weeks (bool): A flag to specify four weeks.
        dir_parent (str): The parent directory.
        dir_name (str): The name of the directory.
        prefix (str): The prefix of the directory.
        suffix (str): The suffix of the directory.
        silent (bool): A flag to silence extraneous messages in console.
    """
    if s_dirs:
        simpledirs(range_, dir_name, prefix, suffix, silent)
        incr_cache_item(key="_mkdirs", silent=silent)
    if dt_dirs:
        date_directories(dir_name, prefix, suffix, silent)
        datedirs(range_, four_weeks, dir_parent, silent)
        incr_cache_item(key="_mkdates", silent=silent)
    if not s_dirs and not dt_dirs:
        print("Void, Please provide a type of directory to make")


@monty.command(name="rm")
@func_time("to remove the directories")
def remove__dirs(
    range_: int = Option(1, "--range", "-r"),
    s_dirs: bool = Option(
        False,
        "--simple-directories",
        "-dirs",
        is_flag=True,
        show_default="range: 1",
    ),
    dt_dirs: bool = Option(
        False,
        "--date-directories",
        "-datedirs",
        is_flag=True,
        show_default="range: 1yr",
    ),
    four_weeks: bool = Option(
        False, "--four-weeks", "-4w", is_flag=True
    ),
    dir_parent: str = Option(None, "--parent", "-p"),
    dir_name: str = Option(None, "--name", show_default="000"),
    prefix: str = Option(None, "--prefix"),
    suffix: str = Option(None, "--suffix"),
    silent: bool = Option(
        False,
        "-s",
        show_default="-!s",
        help="Silence extraneous messages in console",
    ),
):
    """
    Removes folders in the current local directory

    Usage:
        >>> mtax rm -dirs -name 001 -prefix prefix- -suffix -suffix
        >>> mtax rm -datedirs -name 001 -prefix prefix- -suffix -suffix
        >>> mtax rm -dirs -name 001 -prefix prefix- -suffix -suffix -silent
        >>> mtax rm -datedirs -name 001 -prefix prefix- -suffix -suffix -silent
    """
    if s_dirs:
        rmsimpledirs(range_, dir_name, prefix, suffix, silent)
        decr_cache_item(key="_mkdirs", silent=silent)
    if dt_dirs:
        date_directories(dir_name, prefix, suffix, silent)
        rmdatedirs(range_, four_weeks, dir_parent, silent)
        decr_cache_item(key="_mkdates", silent=silent)
    else:
        print("Void, Please provide a type of directory to remove")


@monty.command()
@monty.command(name="help")
@cache_.command(name="help")
@settings_.command(name="help")
def mtax(
    help_: bool = Option(False, "--help", "-h"),
    split: bool = Option(False, "--split"),
    save_funcargs_to_file: bool = Option(False, "--save-a", "-s-a"),
    save_blueprints_to_file: bool = Option(False, "--save-b", "-s-b"),
    save_commands_to_file: bool = Option(False, "--save-c", "-s-c"),
    save_all: bool = Option(False, "--save"),
    func_args: bool = Option(False, "-a", "--args"),
    blueprints: bool = Option(False, "-b", "--blueprints"),
    commands: bool = Option(False, "-c", "--commands"),
    super_silence: bool = Option(False, "-ss", show_default="-!ss"),
    silence: bool = Option(False, "-s", show_default="-!s"),
):
    """Prints the list of MontyAlex commands, their arguments, and their blueprints

    Args:
        help: bool = Option(False, "--help", "-h")
            Print help for the command.
        split: bool = Option(False, "--split")
            Split the lines for better readability.
        save_funcargs_to_file: bool = Option(False, "--save-a", "-s-a")
            Save the arguments of functions to a file.
        save_blueprints_to_file: bool = Option(False, "--save-b", "-s-b")
            Save the blueprints (classes) of functions to a file.
        save_commands_to_file: bool = Option(False, "--save-c", "-s-c")
            Save the commands to a file.
        save_all: bool = Option(False, "--save")
            Save all to a file.
        func_args: bool = Option(False, "-a", "--args")
            Show the arguments of functions.
        blueprints: bool = Option(False, "-b", "--blueprints")
            Show the blueprints (classes) of functions.
        commands: bool = Option(False, "-c", "--commands")
            Show the commands.
        super_silence: bool = Option(False, "-ss", show_default="-!ss")
            Silence all messages in console.
        silence: bool = Option(False, "-s", show_default="-!s")
            Silence extraneous messages in console.
    """
    if help_:
        print("HELP")
    else:
        if not super_silence:
            print(LINEDASH)
            commands_help(
                split, (not blueprints and not func_args) or commands
            )
            if (func_args or blueprints) and commands:
                print(LINEDASH)
            funcargs_help(split, func_args)
            if func_args and blueprints:
                print(LINEDASH)
            blueprints_help(split, blueprints)
            print(LINEDASH)
        save_mtax_commands(
            blueprints=blueprints,
            commands=commands,
            func_args=func_args,
            save_all=save_all,
            save_blueprints=save_blueprints_to_file,
            save_commands=save_commands_to_file,
            save_funcargs=save_funcargs_to_file,
            silence=silence,
            super_silence=super_silence,
        )

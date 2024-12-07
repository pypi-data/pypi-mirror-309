# pylint: disable=line-too-long
# ----------------------------------------------------------------------
# |  _MontyAlex
# ----------------------------------------------------------------------
from montyalex.console_tools import warn_stm
from montyalex.fs_tools import joinpaths, mkdirs, current_working_dir


__version__ = "v0.1.4"


# ----------------------------------------------------------------------
# |  MontyAlex App Commands
# ----------------------------------------------------------------------
mtax_blueprints: list[
    tuple[str, str | None, int | None, str | None]
] = [
    ("├── mtax", "_mtax", "0", None),
    ("├── settings", "us_tools", "4", None),
    (
        "│ ├── init",
        "us_tools.[/][cyan italic]{uo_tools}[/][blue3 dim italic].(schema,json|toml|yaml|mpck).change()",
        "4",
        None,
    ),
    (
        "│ ├── list",
        "us_tools.[/][cyan italic]{uo_tools}[/][blue3 dim italic].(schema,json|toml|yaml|mpck).show_all_values()",
        "4",
        None,
    ),
    (
        "│ ├── delete",
        "us_tools.[/][cyan italic]{uo_tools}[/][blue3 dim italic].(schema,json|toml|yaml|mpck).remove()",
        "4",
        None,
    ),
    (
        "│ └── inspect",
        "us_tools.[/][cyan italic]{uo_tools}[/][blue3 dim italic].(schema,json|toml|yaml|mpck).inspect()",
        "4",
        None,
    ),
    ("├── mk", "directory_tools.single_directory", None, None),
    ("│ ├── [dim](-r/--range)[/]", None, None, None),
    (
        "│ ├── (-dirs/--simple-directories)",
        "directory_tools.simpledirs.create_simple_directories()",
        2,
        None,
    ),
    (
        "│ ├── (-datedirs/--date-directories)",
        "directory_tools.datedirs.create_date_directories()",
        3,
        None,
    ),
    ("│ ├── [dim](-4w/--four-weeks)[/]", None, None, None),
    ("│ ├── [dim](-p/--parent)[/]", None, None, None),
    ("│ ├── [dim](--name)[/]", None, None, None),
    ("│ ├── [dim](--prefix)[/]", None, None, None),
    ("│ ├── [dim](--suffix)[/]", None, None, None),
    ("│ └── [dim](-s)[/]", None, None, None),
    ("├── rm", "directory_tools.single_directory", None, None),
    (
        "│ ├── (-dirs/--simple-directories)",
        "directory_tools.simpledirs.remove_simple_directories()",
        4,
        None,
    ),
    (
        "│ └── (-datedirs/--date-directories)",
        "directory_tools.datedirs.remove_date_directories()",
        5,
        None,
    ),
    ("└── cache", "mtax_cache.MtaxCache", 6, None),
    ("  ├── add", "mtax_cache.MtaxCache.add_item()", None, None),
    ("  ├── clear", "mtax_cache.MtaxCache.clear()", None, None),
    ("  ├── get", "mtax_cache.MtaxCache.get_item()", None, None),
    ("  ├── info", "mtax_cache.MtaxCache.info()", None, None),
    ("  ├── list", "mtax_cache.MtaxCache.list_k_v_pairs()", None, None),
    ("  ├── remove", "mtax_cache.MtaxCache.remove()", None, None),
    ("  ├── reset", "mtax_cache.MtaxCache.reset()", None, None),
    ("  ├── set", "mtax_cache.MtaxCache.set_item()", None, None),
    (
        "  └── time",
        "mtax_cache.MtaxCache.[/][cyan italic]{MtaxTime}[/][blue3 dim italic]",
        None,
        None,
    ),
    ("    ├── reset", "mtax_cache.MtaxCache.timereset()", None, None),
    ("    └── set", "mtax_cache.MtaxCache.timeset()", None, None),
]

mtax_funcargs: list[tuple[str, str, int | str | None, str | None]] = [
    ("├── mtax", None, 6, None),
    (
        "│ ├── [green1 dim](-a)[/]",
        "Shows the arguments of functions",
        ".",
        None,
    ),
    (
        "│ ├── [green1 dim](-b)[/]",
        "Shows the blueprints ([default]classes[/]) of functions",
        ".",
        None,
    ),
    (
        "│ ├── [green1 dim](-c)[/]",
        "Shows the commands while showing args and/or blueprints",
        ".",
        None,
    ),
    (
        "│ ├── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    (
        "│ ├── [green1 dim](--save)[/]",
        "Save a file with the info here for projects or ease of use",
        ".",
        None,
    ),
    (
        "│ └── [green1 dim](--split)[/]",
        "Split the lines for better readability",
        ".",
        None,
    ),
    ("├── settings", None, None, None),
    ("│ ├── init", None, None, None),
    ("│ ├── list", None, None, None),
    ("│ ├── delete", None, None, None),
    ("│ └── inspect", None, None, None),
    ("├── mk", None, 7, None),
    ("│ ├── [green1 dim](-r/--range)[/]", None, ".", None),
    ("│ ├── [dim](-dirs)[/]", None, 6, None),
    ("│ ├── [dim](-datedirs)[/]", None, 3, None),
    ("│ ├── [green1 dim](-4w/--four-weeks)[/]", None, ".", None),
    ("│ ├── [green1 dim](-p/--parent)[/]", None, ".", None),
    ("│ ├── [green1 dim](--name)[/]", None, ".", None),
    ("│ ├── [green1 dim](--prefix)[/]", None, ".", None),
    ("│ ├── [green1 dim](--suffix)[/]", None, ".", None),
    (
        "│ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("├── rm", None, 7, None),
    ("│ ├── [green1 dim](-r/--range)[/]", None, ".", None),
    ("│ ├── [dim](-dirs)[/]", None, 6, None),
    ("│ ├── [dim](-datedirs)[/]", None, 3, None),
    ("│ ├── [green1 dim](-4w/--four-weeks)[/]", None, ".", None),
    ("│ ├── [green1 dim](-p/--parent)[/]", None, ".", None),
    ("│ ├── [green1 dim](--name)[/]", None, ".", None),
    ("│ ├── [green1 dim](--prefix)[/]", None, ".", None),
    ("│ ├── [green1 dim](--suffix)[/]", None, ".", None),
    (
        "│ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("└── cache", None, "0", None),
    ("  ├── add", None, 2, None),
    (
        "  │ ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "  │ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("  ├── clear", None, 2, None),
    (
        "  │ ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "  │ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("  ├── get", None, 2, None),
    (
        "  │ ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "  │ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("  ├── info", None, 2, None),
    (
        "  │ ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "  │ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("  ├── list", None, 2, None),
    (
        "  │ ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "  │ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("  ├── remove", None, 2, None),
    (
        "  │ ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "  │ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("  ├── reset", None, 2, None),
    (
        "  │ ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "  │ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("  ├── set", None, 2, None),
    (
        "  │ ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "  │ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("  └── time", None, "0", None),
    ("    ├── reset", None, 2, None),
    (
        "    │ ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "    │ └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
    ("    └── set", None, 2, None),
    (
        "      ├── [green1 dim](--timezone)[/]",
        "Change the timezone object for time-data",
        ".",
        None,
    ),
    (
        "      └── [green1 dim](-s)[/]",
        "Silence extraneous messages in console",
        ".",
        None,
    ),
]

mtax_commands: list[tuple[str, str, int | None, str | None]] = [
    ("├── mtax", "this command (prints list of commands)", 1, None),
    ("├── settings", "Operations for the settings of mtax", 2, None),
    ("│ ├── init", "Initializes a settings file", 3, None),
    ("│ ├── list", "Lists all mtax components available", 4, None),
    (
        "│ ├── delete",
        "Deletes the settings file or an item from the file",
        5,
        None,
    ),
    (
        "│ └── inspect",
        "Gives a report on info regarding settings in your env",
        6,
        None,
    ),
    (
        "├── mk",
        "Creates a single folder in the current local directory",
        None,
        None,
    ),
    ("│ ├── (-r)", "...", None, None),
    (
        "│ ├── (-dirs)",
        "Creates new blank folders in a range",
        7,
        "default_range: 1",
    ),
    (
        "│ ├── (-datedirs)",
        "Creates new datetime folders in a range",
        8,
        "default_range: *1yr",
    ),
    ("│ ├── (-4w)", "...", None, None),
    ("│ ├── (-p)", "...", None, None),
    ("│ ├── (--name)", "...", None, None),
    ("│ ├── (--prefix)", "...", None, None),
    ("│ ├── (--suffix)", "...", None, None),
    ("│ └── (-s)", "...", None, None),
    (
        "├── rm",
        "Removes a single folder in the current local directory",
        None,
        None,
    ),
    (
        "│ ├── (-dirs)",
        "Removes blank folders in a range",
        9,
        "default_range: 1",
    ),
    (
        "│ └── (-datedirs)",
        "Removes datetime folders in a range",
        10,
        "default_range: *1yr",
    ),
    ("└── cache", "Operations for the cache of mtax", None, None),
    (" ├── add", "Add to the cache", 11, None),
    (" ├── clear", "Clear the cache", 12, None),
    (" ├── get", "Gets an item from the cache", 13, None),
    (" ├── info", "Shows various info about the cache", 14, None),
    (" ├── list", "List the items stored in the cache", 15, None),
    (
        " ├── remove",
        "Remove the matching item from the cache",
        16,
        None,
    ),
    (" ├── reset", "Reset stuck items in the cache", 17, None),
    (" ├── set", "Set a item in the cache (Overwrite)", 18, None),
    (" └── time", "Manage time-data in the cache", None, None),
    ("    ├── reset", "Reset time-data in the cache", 19, None),
    (
        "    └── set",
        "Set a timestamp to time-data in the cache",
        20,
        None,
    ),
]


# ----------------------------------------------------------------------
# |  Save MontyAlex App Commands Markdown
# ----------------------------------------------------------------------
def mtax_complete(
    *,
    commands: bool = True,
    func_args: bool = False,
    blueprints: bool = False,
):
    mtax_available: list[str] = [
        "## `mtax`\n\n",
        "### `mtax --split`\n\n",
        "### `mtax --save`\n\n",
        "### `mtax -a`\n\n",
        "### `mtax -b`\n\n",
        "### `mtax -c`\n\n",
        "### `mtax -s`\n\n",
        "## `settings`\n\n",
        "### `settings init`\n\n",
        "### `settings list`\n\n",
        "### `settings delete`\n\n",
        "### `settings inspect`\n\n",
        "## `mk`\n\n",
        "### `mk -dirs`\n\n",
        "### `mk -datedirs`\n\n",
        "## `rm`\n\n",
        "### `rm -dirs`\n\n",
        "### `rm -datedirs`\n\n",
        "## `cache`\n\n",
        "## `cache add`\n\n",
        "## `cache clear`\n\n",
        "## `cache get`\n\n",
        "## `cache info`\n\n",
        "## `cache list`\n\n",
        "## `cache remove`\n\n",
        "## `cache reset`\n\n",
        "## `cache set`\n\n",
        "## `cache time`\n\n",
        "## `cache time reset`\n\n",
        "## `cache time set`\n\n",
    ]

    available: list[str] = [
        "The command that prints a list of commands (or generates this file)\n\n",
        "...\n\n",
        "...\n\n",
        "...\n\n",
        "...\n\n",
        "...\n\n",
        "...\n\n",
        "settings...\n\n",
        "init...\n\n",
        "list...\n\n",
        "delete...\n\n",
        "inspect...\n\n",
        "Creates a single folder in the current local directory\n\n",
        "Creates new blank folders in a range\n\n",
        "Creates new datetime folders in a range\n\n",
        "Removes a single folder in the current local directory\n\n",
        "Removes blank folders in a range\n\n",
        "Removes datetime folders in a range\n\n",
        "Operations for the cache of mtax\n\n",
        "Add to the cache\n\n",
        "Clear the cache\n\n",
        "Gets an item from the cache\n\n",
        "Shows various info about the cache\n\n",
        "List the items stored in the cache\n\n",
        "Remove the matching item from the cache\n\n",
        "Reset stuck items in the cache\n\n",
        "Set a item in the cache (Overwrite)\n\n",
        "Manage time-data in the cache\n\n",
        "Reset time-data in the cache\n\n",
        "Set a timestamp to time-data in the cache\n\n",
    ]
    templates: list[str] = [
        "  `...`\n\n",
        "  None\n\n",
        "  None\n\n",
        "  None\n\n",
        "  None\n\n",
        "  None\n\n",
        "  None\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  None\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
        "  `...`\n\n",
    ]
    arguments: list[str] = [
        "- [--split]\n- [-s-a]\n- [-s-b]\n- [-s-c]\n- [--save]\n- [-a]\n- [-b]\n- [-c]\n- [-s]\n- [-ss]\n",
        "None\n",
        "None\n",
        "None\n",
        "None\n",
        "None\n",
        "None\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "None\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
        "- ...\n",
    ]

    if commands:
        mtax_available = [
            item + desc for item, desc in zip(mtax_available, available)
        ]
    if blueprints:
        mtax_available = [
            item + desc for item, desc in zip(mtax_available, templates)
        ]
    if func_args:
        mtax_available = [
            item + desc for item, desc in zip(mtax_available, arguments)
        ]

    cwd = joinpaths(current_working_dir, ".mtax")
    cmd_fd = joinpaths(cwd, "commands.md")

    mkdirs(cwd, exist_ok=True)
    with open(cmd_fd, "w", encoding="UTF-8") as commands_file:
        commands_file.write(
            f"# MontyAlex\n\nA list of all mtax commands available as of {__version__}\n\n"
        )
        commands_file.writelines("\n".join(mtax_available))


def save_mtax_commands(
    *,
    blueprints: bool = False,
    commands: bool = False,
    func_args: bool = False,
    save_all: bool = False,
    save_commands: bool = False,
    save_funcargs: bool = False,
    save_blueprints: bool = False,
    silence: bool = False,
    super_silence: bool = False,
):
    """
    Save MontyAlex commands, function arguments, and blueprints to a markdown file.

    Args:
        blueprints (bool): Whether to include blueprints in the output.
        commands (bool): Whether to include commands in the output.
        func_args (bool): Whether to include function arguments in the output.
        save_all (bool): Save all information (commands, args, blueprints) to the file.
        save_commands (bool): Save only commands to the file.
        save_funcargs (bool): Save only function arguments to the file.
        save_blueprints (bool): Save only blueprints to the file.
        silence (bool): Suppress warnings and info messages.
        super_silence (bool): Suppress all console output.
    """
    if save_commands:
        mtax_complete(commands=True, func_args=False, blueprints=False)
    if save_funcargs:
        mtax_complete(commands=False, func_args=True, blueprints=False)
    if save_blueprints:
        mtax_complete(commands=False, func_args=False, blueprints=True)
    if save_all:
        mtax_complete(
            commands=commands,
            func_args=func_args,
            blueprints=blueprints,
        )
        if not silence and not super_silence:
            print(
                f"{warn_stm}, Syntax highlighting is not supported in files"
            )

from montyalex._mtax import (
    mtax_blueprints,
    mtax_commands,
    mtax_funcargs,
)
from montyalex.typing_tools import NoneType


def commands_help(split: bool = False, commands: bool = False):
    if commands:
        if split:
            print("")
        print("cmds.")
        if split:
            print("")
        for name, shorthelp, index, defaults in mtax_commands:
            if isinstance(index, int):
                if index <= 9:
                    helpmsg = f"([pink3 dim]{index}[/]) {name} -> [dim italic]{shorthelp}[/]"
                else:
                    helpmsg = f"([pink3 dim]{index}[/]){name} -> [dim italic]{shorthelp}[/]"
            if isinstance(index, NoneType):
                helpmsg = (
                    f"([dim]X[/]) {name} -> [dim italic]{shorthelp}[/]"
                )
            if defaults:
                helpmsg += f" [pink3 dim italic]({defaults})[/]"
            print(helpmsg)
            if split:
                print("")


def funcargs_help(split: bool = False, func_args: bool = False):
    if func_args:
        if split:
            print("")
        print("args.")
        if split:
            print("")
        for (
            func,
            module,
            funcargs_index,
            funcargs_defaults,
        ) in mtax_funcargs:
            if funcargs_index:
                if funcargs_index != ".":
                    helpmsg = f"([green1 dim]{funcargs_index}[/]) [italic]{func}[/]"
                else:
                    helpmsg = (
                        f"([dim]{funcargs_index}[/]) [italic]{func}[/]"
                    )
            else:
                helpmsg = f"    [italic]{func}[/]"
            if module:
                helpmsg += f" -> [green1 dim italic]{module}[/]"
            if funcargs_defaults:
                helpmsg += f" [dim italic]({funcargs_defaults})[/]"
            if not module and not funcargs_defaults:
                helpmsg += " [dim italic]...[/]"
            print(helpmsg)
            if split:
                print("")


def blueprints_help(split: bool = False, blueprints: bool = False):
    if blueprints:
        if split:
            print("")
        print("bpns.")
        if split:
            print("")
        for (
            blueprint,
            module,
            blueprint_index,
            blueprint_defaults,
        ) in mtax_blueprints:
            if blueprint_index:
                helpmsg = (
                    f"([blue3 dim]{blueprint_index}[/]) {blueprint}"
                )
            else:
                helpmsg = f"    {blueprint}"
            if module:
                helpmsg += f" -> [blue3 dim italic]{module}[/]"
            if blueprint_defaults:
                helpmsg += f" [dim italic]({blueprint_defaults})[/]"
            if not module and not blueprint_defaults:
                helpmsg += " [dim italic]...[/]"
            print(helpmsg)
            if split:
                print("")

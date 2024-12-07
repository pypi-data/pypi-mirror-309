# ----------------------------------------------------------------------
# |  _Settings
# ----------------------------------------------------------------------
from .console_tools import richconsole
from .typer_helpers import (
    delete_useroptions,
    initialize_useroptions,
    inspect_useroptions,
)
from .typer_tools import Option, Typer
from .us_tools import SETTINGS

print = richconsole.print


# ----------------------------------------------------------------------
# |  Typer App
# ----------------------------------------------------------------------
settings_: Typer = Typer(
    name="settings",
    add_help_option=False,
    pretty_exceptions_show_locals=False,
)


# ----------------------------------------------------------------------
# |  Typer Commands; init_, list_, delete_, inspect_
# ----------------------------------------------------------------------
@settings_.command(name="list", add_help_option=False)
def list_(
    repr_listing: bool = Option(False, "--repr", "-r"),
):
    """List the current settings

    Args:
        repr_listing (bool): If True, print the repr representation of SETTINGS;
                             otherwise, show all values.
    """
    if repr_listing:
        print(f"{SETTINGS!r}")
    else:
        SETTINGS.show_all_values()


@settings_.command(name="init", add_help_option=False)
@settings_.command(name="init", add_help_option=False)
def init_(
    dirname: str = Option(".mtax", "--directory-name", "-dir"),
    filename: str = Option("settings", "--file-name", "-name"),
    *,
    overwrite: bool = Option(False, "--overwrite", "-o"),
    use_all: bool = Option(False, "--all", "-a"),
    use_synced: bool = Option(False, "--sync", "-s"),
    use_json: bool = Option(False, "--json", "-j"),
    use_toml: bool = Option(False, "--toml", "-t"),
    use_yaml: bool = Option(False, "--yaml", "-y"),
    use_mpck: bool = Option(False, "--mpck", "-m"),
):
    """Initialize settings file

    Args:
        dirname (str): The directory to put the settings file in.
        filename (str): The name of the settings file.
        overwrite (bool): If True, overwrite the existing file.
        use_all (bool): If True, use all formats.
        use_synced (bool): If True, use the synced format.
        use_json (bool): If True, use the JSON format.
        use_toml (bool): If True, use the TOML format.
        use_yaml (bool): If True, use the YAML format.
        use_mpck (bool): If True, use the MPCK format.
    """
    initialize_useroptions(
        dirname=dirname,
        filename=filename,
        overwrite=overwrite,
        use_all=use_all,
        use_synced=use_synced,
        use_json=use_json,
        use_toml=use_toml,
        use_yaml=use_yaml,
        use_mpck=use_mpck,
    )


@settings_.command(name="delete", add_help_option=False)
def delete_(
    dirname: str = Option(".mtax", "--directory-name", "-dir"),
    filename: str = Option("settings", "--file-name", "-name"),
    key: str = Option(None, "--key", "-k"),
    *,
    use_json: bool = Option(False, "--json", "-j"),
    use_toml: bool = Option(False, "--toml", "-t"),
    use_yaml: bool = Option(False, "--yaml", "-y"),
    use_mpck: bool = Option(False, "--mpck", "-m"),
):
    """Delete settings file or a key from settings file

    Args:
        dirname (str): The directory to put the settings file in.
        filename (str): The name of the settings file.
        key (str): The key to delete from the settings file.
        use_json (bool): If True, use the JSON format.
        use_toml (bool): If True, use the TOML format.
        use_yaml (bool): If True, use the YAML format.
        use_mpck (bool): If True, use the MPCK format.
    """
    delete_useroptions(
        dirname=dirname,
        filename=filename,
        key=key,
        use_json=use_json,
        use_toml=use_toml,
        use_yaml=use_yaml,
        use_mpck=use_mpck,
    )


@settings_.command(name="inspect", add_help_option=False)
def inspect_(
    dirname: str = Option(".mtax", "--directory-name", "-dir"),
    filename: str = Option("settings", "--file-name", "-name"),
    use_all: bool = Option(False, "--all", "-a"),
    use_synced: bool = Option(False, "--sync", "-s"),
    use_json: bool = Option(False, "--json", "-j"),
    use_toml: bool = Option(False, "--toml", "-t"),
    use_yaml: bool = Option(False, "--yaml", "-y"),
    use_mpck: bool = Option(False, "--mpck", "-m"),
    full_inspection: bool = Option(False, "--full", "-fi"),
    mem_alloc_inspection: bool = Option(False, "--memory", "-mi"),
    repr_inspection: bool = Option(False, "--repr", "-ri"),
    exists_inspection: bool = Option(False, "--exists", "-ei"),
    key_inspection: str = Option(None, "--key", "-ki"),
) -> None:
    """Inspect settings file

    Args:
        dirname (str): The directory to put the settings file in.
        filename (str): The name of the settings file.
        use_all (bool): If True, use all formats.
        use_synced (bool): If True, use the synced format.
        use_json (bool): If True, use the JSON format.
        use_toml (bool): If True, use the TOML format.
        use_yaml (bool): If True, use the YAML format.
        use_mpck (bool): If True, use the MPCK format.
        full_inspection (bool): If True, inspect the entire file.
        mem_alloc_inspection (bool): If True, inspect the memory allocation.
        repr_inspection (bool): If True, inspect the representation.
        exists_inspection (bool): If True, inspect if the file exists.
        key_inspection (str): The key to inspect.
    """
    inspect_useroptions(
        dirname,
        filename,
        use_all=use_all,
        use_synced=use_synced,
        use_json=use_json,
        use_toml=use_toml,
        use_yaml=use_yaml,
        use_mpck=use_mpck,
        full_inspection=full_inspection,
        mem_alloc_inspection=mem_alloc_inspection,
        repr_inspection=repr_inspection,
        exists_inspection=exists_inspection,
        key_inspection=key_inspection,
    )

from montyalex.typer_tools import Option
from montyalex.uo_tools import json, toml, yaml, mpck
from .init_objects import (
    default_settings_template,
    empty_settings_plus_fmt,
    empty_settings_template,
)
from .initialization import initialize_schema


def initialize_useroptions(
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
    uo: json | toml | yaml | mpck | None = None
    if use_json:
        uo = json(directory=dirname, filename=filename)
    if use_toml:
        uo = toml(directory=dirname, filename=filename)
    if use_yaml:
        uo = yaml(directory=dirname, filename=filename)
    if use_mpck:
        uo = mpck(directory=dirname, filename=filename)
    if uo is None:
        uo = json(directory=dirname, filename=filename)

    if not use_all or use_synced:
        if overwrite:
            if isinstance(uo, json):
                uo.change("$schema", "./schema.json")
                initialize_schema(dirname)
            uo.change("mtax", default_settings_template, append=False)
        else:
            if isinstance(uo, json):
                uo.change("$schema", "./schema.json")
                initialize_schema(dirname)
            if isinstance(uo, toml):
                uo.change("mtax", empty_settings_plus_fmt)
            else:
                uo.change("mtax", default_settings_template)
    else:
        juo = json(directory=dirname, filename=filename)
        tuo = toml(directory=dirname, filename=filename)
        yuo = yaml(directory=dirname, filename=filename)
        muo = mpck(directory=dirname, filename=filename)
        if overwrite:
            juo.change("$schema", "./schema.json")
            initialize_schema(dirname)
            juo.change("mtax", default_settings_template)
            tuo.change("mtax", empty_settings_template, append=False)
            yuo.change("mtax", default_settings_template, append=False)
            muo.change("mtax", default_settings_template, append=False)
        else:
            juo.change("$schema", "./schema.json")
            initialize_schema(dirname)
            juo.change("mtax", default_settings_template)
            tuo.change("mtax", empty_settings_template)
            yuo.change("mtax", default_settings_template)
            muo.change("mtax", default_settings_template)

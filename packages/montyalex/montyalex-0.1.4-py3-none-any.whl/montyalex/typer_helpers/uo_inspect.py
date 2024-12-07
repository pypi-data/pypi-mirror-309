from montyalex.typer_tools import Option
from montyalex.uo_tools import json, toml, yaml, mpck
from montyalex.us_tools import SETTINGS
from .initialization import initialize_void


def inspect_useroptions(
    dirname: str = Option(".mtax", "--directory-name", "-dir"),
    filename: str = Option("settings", "--file-name", "-name"),
    *,
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
):
    uo: json | toml | yaml | mpck | None = None
    if use_json:
        juo: json = json(directory=dirname, filename=filename)
        uo = juo
    if use_toml:
        tuo: toml = toml(directory=dirname, filename=filename)
        uo = tuo
    if use_yaml:
        yuo: yaml = yaml(directory=dirname, filename=filename)
        uo = yuo
    if use_mpck:
        muo: mpck = mpck(directory=dirname, filename=filename)
        uo = muo
    if uo is None:
        uo = json(directory=dirname, filename=filename)

    inspection: bool = False
    initialize_void(
        uo,
        dirname,
        filename,
        use_all=use_all,
        use_synced=use_synced,
        use_json=use_json,
        use_toml=use_toml,
        use_yaml=use_yaml,
        use_mpck=use_mpck,
    )
    if full_inspection:
        inspection = True
        uo.inspect(full=True)
        print("[green]Verified Settings:[/]")
        print(f"{SETTINGS!r}")
        SETTINGS.show_all_values()
        # if repr_listing:
        #     print(f'{SETTINGS!r}')
        # else:
        #     print(f'{SETTINGS!r}')
        #     SETTINGS.show_all_values()
    if mem_alloc_inspection:
        inspection = True
        uo.inspect(mem_alloc=True)
    if repr_inspection:
        inspection = True
        uo.inspect(representation=True)
    if key_inspection:
        inspection = True
        uo.inspect(key=key_inspection)
    if exists_inspection:
        inspection = True
        if uo.exists:
            print(f"Found! [green]{uo.modelpath}[/]")
        else:
            print(f"Not Found! [red]{uo.modelpath}[/]")
    if not inspection:
        uo.inspect()

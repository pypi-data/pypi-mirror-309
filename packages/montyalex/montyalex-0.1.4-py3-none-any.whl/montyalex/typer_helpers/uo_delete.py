from montyalex.typer_tools import Option
from montyalex.uo_tools import json, toml, yaml, mpck


def delete_useroptions(
    dirname: str = Option(".mtax", "--directory-name", "-dir"),
    filename: str = Option("settings", "--file-name", "-name"),
    key: str = Option(None, "--key", "-k"),
    *,
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

    if key:
        uo.change(key, None, overwrite=True)
    uo.remove()

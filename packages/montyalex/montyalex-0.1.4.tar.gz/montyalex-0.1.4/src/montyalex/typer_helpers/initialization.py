from montyalex.uo_tools import schema, json, toml, yaml, mpck
from .init_objects import settings_schema_definition
from .uo_init import initialize_useroptions


def initialize_schema(dirname: str = ".mtax", filename: str = "schema"):
    _schema = schema(directory=dirname, filename=filename)
    _schema.change("$schema", "http://json-schema.org/draft-07/schema#")
    _schema.change("$id", "montyalex.python-cli.settings-v0.1.4")
    _schema.change("title", "Settings")
    _schema.change("description", "MontyAlex CLI Settings")
    _schema.change("type", "object")
    _schema.change("properties", {"mtax": settings_schema_definition})
    _schema.change("required", ["mtax"])


def initialize_void(
    uo: json | toml | yaml | mpck,
    dirname: str,
    filename: str,
    *,
    use_all: bool,
    use_synced: bool,
    use_json: bool,
    use_toml: bool,
    use_yaml: bool,
    use_mpck: bool,
):
    if not uo.exists:
        print("Creating new settings file...")
        initialize_useroptions(
            dirname=dirname,
            filename=filename,
            overwrite=False,
            use_all=use_all,
            use_synced=use_synced,
            use_json=use_json,
            use_toml=use_toml,
            use_yaml=use_yaml,
            use_mpck=use_mpck,
        )

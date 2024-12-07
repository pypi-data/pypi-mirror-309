default_settings_template = {
    "action.dirs.datetime": {
        "default.opt.four-week-month": False,
        "default.opt.format": "%Y-%m-%d",
        "default.opt.range": "1yr",
    },
    "action.dirs.simple": {"default.opt.range": 1},
    "action.opt.silent": False,
    "default.info.timezone": None,
    "user.locale.city": None,
    "user.locale.continent": None,
    "user.locale.country": None,
    "user.locale.state": None,
    "user.locale.street-name": None,
    "user.locale.street-number": None,
}

empty_settings_template = {
    "action.dirs.datetime": {
        "default.opt.four-week-month": False,
        "default.opt.range": "1yr",
    },
    "action.dirs.simple": {"default.opt.range": 1},
    "action.opt.silent": False,
    "default.info.timezone": "",
    "user.locale.city": "",
    "user.locale.continent": "",
    "user.locale.country": "",
    "user.locale.state": "",
    "user.locale.street-name": "",
    "user.locale.street-number": "",
}

empty_settings_plus_fmt = {
    "action.dirs.datetime": {
        "default.opt.four-week-month": False,
        "default.opt.format": "%Y-%m-%d",
        "default.opt.range": "1yr",
    },
    "action.dirs.simple": {"default.opt.range": 1},
    "action.opt.silent": False,
    "default.info.timezone": "",
    "user.locale.city": "",
    "user.locale.continent": "",
    "user.locale.country": "",
    "user.locale.state": "",
    "user.locale.street-name": "",
    "user.locale.street-number": "",
}

settings_schema_definition = {
    "description": "",
    "type": "object",
    "properties": {
        "action.dirs.datetime": {
            "description": "",
            "type": "object",
            "properties": {
                "default.opt.four-week-month": {
                    "description": "Use a four week (28d) range instead of a complete month",
                    "type": ["boolean", "null"],
                    "default": False,
                },
                "default.opt.format": {
                    "description": "Change the date format used for folders",
                    "type": ["string", "null"],
                    "default": "%Y-%m-%d",
                },
                "default.opt.range": {
                    "description": "",
                    "type": ["string", "null"],
                    "default": "1yr",
                },
            },
        },
        "action.dirs.simple": {
            "description": "",
            "type": "object",
            "properties": {
                "default.opt.range": {
                    "description": "",
                    "type": ["integer", "null"],
                    "default": 1,
                }
            },
        },
        "action.opt.silent": {
            "description": "",
            "type": ["boolean", "null"],
            "default": False,
        },
        "default.info.timezone": {
            "description": "Default timezone used for date related commands",
            "type": ["string", "null"],
        },
    },
}

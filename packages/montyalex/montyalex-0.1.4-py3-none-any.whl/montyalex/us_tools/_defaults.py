# ----------------------------------------------------------------------
# |  _Defaults
# ----------------------------------------------------------------------
from ._components import (
    GroupSettingName,
    ShortSettingName,
    SettingName,
    SettingComponent,
)
from ._actions import datetime_directory_action, simple_directory_action


# ----------------------------------------------------------------------
# |  Default Setting Component
# ----------------------------------------------------------------------
class Default(SettingComponent):
    """
    A Default setting component represents a default setting.

    It is defined by an infix, suffix, type, and optionally a prefix and parent.

    The prefix and infix are used to construct the setting's identifier.
    The parent is an instance of a setting name class that provides hierarchical context.
    The type is used to validate associated values.
    """

    def __init__(
        self,
        infix: str,
        suffix: str,
        type_: type,
        *,
        prefix: str = "default",
        parent: (
            GroupSettingName | ShortSettingName | SettingName
        ) = None,
    ) -> None:
        super().__init__(
            prefix, infix, suffix, type_=type_, parent=parent
        )


# ----------------------------------------------------------------------
# |  Default Instances
# ----------------------------------------------------------------------
timezone_info_default = Default(
    "info",
    "timezone",
    str,
    parent=SettingName("default", "info", "timezone"),
)
timeout_option_default = Default(
    "opt",
    "timeout",
    str,
    parent=SettingName("default", "opt", "timeout"),
)
fourweek_option_default = Default(
    "opt", "four-week-month", bool, parent=datetime_directory_action
)
datetime_range_option_default = Default(
    "opt", "range", str, parent=datetime_directory_action
)
datetime_format_option_default = Default(
    "opt", "format", str, parent=datetime_directory_action
)
simple_range_option_default = Default(
    "opt", "range", str, parent=simple_directory_action
)

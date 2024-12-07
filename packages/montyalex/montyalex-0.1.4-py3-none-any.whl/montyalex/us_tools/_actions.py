# ----------------------------------------------------------------------
# |  _Actions
# ----------------------------------------------------------------------
from ._components import (
    GroupSettingName,
    ShortSettingName,
    SettingName,
    SettingComponent,
)


# ----------------------------------------------------------------------
# |  Action Setting Component
# ----------------------------------------------------------------------
class Action(SettingComponent):
    """An Action setting component represents a specific action-related setting.

    It is defined by an infix, suffix, type, and optionally a prefix and parent.

    The prefix, infix, and suffix are used to construct the setting's identifier.
    The parent is an instance of a setting name class that provides hierarchical context.
    The type is used to validate associated values.
    """

    def __init__(
        self,
        infix: str,
        suffix: str,
        type_: type,
        *,
        prefix: str = "action",
        parent: (
            GroupSettingName | ShortSettingName | SettingName
        ) = None,
    ) -> None:
        super().__init__(
            prefix, infix, suffix, type_=type_, parent=parent
        )


# ----------------------------------------------------------------------
# |  Action Instances
# ----------------------------------------------------------------------
datetime_directory_action = Action(
    "dirs",
    "datetime",
    object,
    parent=SettingName("action", "dirs", "datetime"),
)
simple_directory_action = Action(
    "dirs",
    "simple",
    object,
    parent=SettingName("action", "dirs", "simple"),
)
silent_option_action = Action(
    "opt", "silent", bool, parent=SettingName("action", "opt", "silent")
)

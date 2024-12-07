# ----------------------------------------------------------------------
# |  _User-Info
# ----------------------------------------------------------------------
from ._components import (
    GroupSettingName,
    ShortSettingName,
    SettingName,
    SettingComponent,
)


# ----------------------------------------------------------------------
# |  User Info Setting Component
# ----------------------------------------------------------------------
class UserInfo(SettingComponent):
    """A UserInfo setting component represents a specific user-related setting.

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
        prefix: str = "user",
        parent: (
            GroupSettingName | ShortSettingName | SettingName
        ) = None,
    ) -> None:
        super().__init__(
            prefix, infix, suffix, type_=type_, parent=parent
        )


# ----------------------------------------------------------------------
# |  User Locale Instances
# ----------------------------------------------------------------------
locale_continent_userinfo = UserInfo(
    "locale",
    "continent",
    str,
    parent=SettingName("user", "locale", "continent"),
)
locale_country_userinfo = UserInfo(
    "locale",
    "country",
    str,
    parent=SettingName("user", "locale", "country"),
)
locale_region_userinfo = UserInfo(
    "locale",
    "region",
    str,
    parent=SettingName("user", "locale", "region"),
)
locale_state_userinfo = UserInfo(
    "locale",
    "state",
    str,
    parent=SettingName("user", "locale", "state"),
)
locale_province_userinfo = UserInfo(
    "locale",
    "province",
    str,
    parent=SettingName("user", "locale", "province"),
)
locale_city_userinfo = UserInfo(
    "locale", "city", str, parent=SettingName("user", "locale", "city")
)
locale_streetname_userinfo = UserInfo(
    "locale",
    "street-name",
    str,
    parent=SettingName("user", "locale", "street-name"),
)
locale_streetnum_userinfo = UserInfo(
    "locale",
    "street-number",
    str,
    parent=SettingName("user", "locale", "street-number"),
)

# ----------------------------------------------------------------------
# |  Category
# ----------------------------------------------------------------------
from ._components import GroupSettingName as Group
from .subcategory import (
    SettingSubcategory as Subcategory,
    option_action_subcategory,
    info_default_subcategory,
    option_default_subcategory,
    locale_userinfo_subcategory,
)


# ----------------------------------------------------------------------
# |  Setting Category
# ----------------------------------------------------------------------
class SettingCategory:
    """
    A SettingCategory represents a category of settings within a
    settings container.

    It is defined by a prefix, type, and a variable number of
    subcategories.

    The prefix and infix are used to construct the ``info`` attribute,
    which is an instance of ``GroupSettingName``. This is used to
    identify the category.

    The type is a type that is used to check if a value is valid for
    the category.

    The subcategories are a tuple of instances of ``SettingSubcategory``.
    These are used to construct the settings within the category.

    The ``add_subcategory`` method is used to add additional subcategories
    to the category.

    The ``__str__`` method is used to get a string representation of the
    category, which is the string representation of the subcategories.

    The ``__repr__`` method is used to get a string representation of the
    category that can be evaluated as Python code.
    """

    def __init__(
        self, prefix: str, type_: type, *subcategories: Subcategory
    ) -> None:
        self.info: Group = Group(prefix)
        self.type_: type = type_
        self.subcategories: tuple[Subcategory] = subcategories

    def __str__(self) -> str:
        return f"{self.subcategories}"

    def __repr__(self) -> str:
        subcategories = f"{list(self.subcategories)!r}"
        return f"Category(={self.info.prefix}, type={self.type_}, subcategories={subcategories})"

    def add_subcategory(self, subcategory: Subcategory) -> None:
        new_subcategories = (*self.subcategories, subcategory)
        self.subcategories = new_subcategories


# ----------------------------------------------------------------------
# |  Categories
# ----------------------------------------------------------------------
ACTION = SettingCategory("action", object, option_action_subcategory)
DEFAULT = SettingCategory(
    "default",
    object,
    info_default_subcategory,
    option_default_subcategory,
)
USERINFO = SettingCategory("user", object, locale_userinfo_subcategory)

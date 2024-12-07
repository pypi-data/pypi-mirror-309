# ----------------------------------------------------------------------
# |  Decorators
# ----------------------------------------------------------------------
from montyalex.fs_tools import cancel
from montyalex.object_tools import Key, Value, RangeError
from montyalex.typing_tools import Any, Callable, Literal
from montyalex.uo_tools import yaml


# ----------------------------------------------------------------------
# |  State-Manager
# ----------------------------------------------------------------------
def statemanager_decorator(
    key: Key, value: Value, file_name: str, *, loc: str = None
):
    """
    A decorator that saves the given key-value pair in a YAML file
    and prints the state before calling the function.

    Args:
        key (Key): A key for the state.
        value (Value): The value for the key.
        file_name (str): The name of the YAML file.
        loc (str, optional): The location of the YAML file. Defaults to ".mtax".

    Returns:
        Callable[[Callable], Callable]: A decorator.
    """
    yaml_state = yaml(
        directory=loc if loc else ".mtax", filename=file_name
    )

    def statemanager(func):
        state: dict[Key, Any] = {key: value}

        def wrapper():
            print(f"{state}")
            func()

        yaml_state.model(state, write=True, overwrite=True)
        return wrapper

    print(yaml_state.modelpath)
    return statemanager


# ----------------------------------------------------------------------
# |  State-Modifier Helper Function for Incr/Decr
# ----------------------------------------------------------------------
def statemodifier(
    value: Value,
    operation: Literal[0] | Literal[1],
    multiplier: int = 1,
    limit: int | tuple[int, int] = None,
    ilimit: int | tuple[int, int] = None,
) -> bool:
    """
    A helper function for state modification. It checks if the given value
    is within the given limit or inclusive limit after the given operation.
    If it is not, it raises a RangeError.

    Args:
        value (Value): The value to check.
        operation (Literal[0] | Literal[1]): The operation to perform.
            0 for increment, 1 for decrement.
        multiplier (int, optional): The multiplier for the operation.
            Defaults to 1.
        limit (int | tuple[int, int], optional): The limit for the value.
            Defaults to None.
        ilimit (int | tuple[int, int], optional): The inclusive limit for the value.
            Defaults to None.

    Raises:
        RangeError: If the value is not within the given limit or inclusive limit.

    Returns:
        bool: True if the value is within the given limit or inclusive limit.
    """
    if isinstance(limit, tuple) or isinstance(ilimit, tuple):
        range_limit = (
            range(*limit)
            if not ilimit
            else range(ilimit[0], ilimit[1] + 1)
        )
        check = (
            value + multiplier if operation == 0 else value - multiplier
        )
        if value not in range_limit or check not in range_limit:
            if limit:
                raise RangeError(
                    f"Index ({check}) not in", range(*limit)
                )
            if ilimit:
                raise RangeError(
                    f"Index ({check}) not in", range(*ilimit)
                )
            cancel()
    if isinstance(limit, int) or isinstance(ilimit, int):
        range_limit = range(limit) if not ilimit else range(ilimit + 1)
        check = (
            value + multiplier if operation == 0 else value - multiplier
        )
        if value not in range_limit or check not in range_limit:
            if limit:
                raise RangeError(
                    f"Index ({check}) not in", range(limit)
                )
            if ilimit:
                raise RangeError(
                    f"Index ({check}) not in", range(ilimit)
                )
            cancel()
    return True


# ----------------------------------------------------------------------
# |  State-Decr (-multiplier)
# ----------------------------------------------------------------------
def statedecr_decorator(
    key: Key,
    file_name: str,
    *,
    multiplier: int = 1,
    limit: int | tuple[int, int] = None,
    ilimit: int | tuple[int, int] = None,
    loc: str = None,
):
    """
    Decorator to decrement a value in a settings file.

    Args:
        key (Key): The key to decrement.
        file_name (str): The name of the settings file.
        multiplier (int, optional): The multiplier for the decrement. Defaults to 1.
        limit (int | tuple[int, int], optional): The limit for the decrement. Defaults to None.
        ilimit (int | tuple[int, int], optional): The inclusive limit for the decrement. Defaults to None.
        loc (str, optional): The location of the settings file. Defaults to None.

    Returns:
        Callable[[Callable], Callable]: The decorated function.
    """
    yaml_state = yaml(
        directory=loc if loc else ".mtax", filename=file_name
    )

    def statedecrementer(func):
        key_value = yaml_state.model(read=True)[key]
        state: dict[Key, Any] = {}
        if isinstance(key_value, int):
            state: dict[Key, Any] = {key: key_value - multiplier}

        def wrapper():
            func()

        try:
            smdecr = statemodifier(
                key_value, 1, multiplier, limit, ilimit
            )
            if state[key] != key_value and smdecr:
                print(f"{state}")
                yaml_state.model(state, write=True, overwrite=True)
                print(yaml_state.modelpath)
        except RangeError as e:
            print(e)
        return wrapper

    return statedecrementer


# ----------------------------------------------------------------------
# |  State-Incr (+multiplier)
# ----------------------------------------------------------------------
def stateincr_decorator(
    key: Key,
    file_name: str,
    *,
    multiplier: int = 1,
    limit: int | tuple[int, int] = None,
    ilimit: int | tuple[int, int] = None,
    loc: str = None,
) -> Callable[[Callable], Callable]:
    """
    Decorator to increment a value in a settings file.

    Args:
        key (Key): The key to increment.
        file_name (str): The name of the settings file.
        multiplier (int, optional): The multiplier for the increment. Defaults to 1.
        limit (int | tuple[int, int], optional): The limit for the increment. Defaults to None.
        ilimit (int | tuple[int, int], optional): The inclusive limit for the increment. Defaults to None.
        loc (str, optional): The location of the settings file. Defaults to None.

    Returns:
        Callable[[Callable], Callable]: The decorated function.
    """
    yaml_state = yaml(
        directory=loc if loc else ".mtax", filename=file_name
    )

    def stateincrementer(func):
        key_value = yaml_state.model(read=True)[key]
        state: dict[Key, Any] = {}
        if isinstance(key_value, int):
            state: dict[Key, Any] = {key: key_value + multiplier}

        def wrapper():
            func()

        try:
            smincr = statemodifier(
                key_value, 0, multiplier, limit, ilimit
            )
            if state[key] != key_value and smincr:
                print(f"{state}")
                yaml_state.model(state, write=True, overwrite=True)
                print(yaml_state.modelpath)
        except RangeError as e:
            print(e)
        return wrapper

    return stateincrementer

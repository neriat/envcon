import json
import re
from typing import Final, Union, get_args, get_origin, List, Any

from .functional import first

try:
    # list[T], dict[T,U] etc'. python 38 compatibility
    from types import GenericAlias as _GenericAlias  # type: ignore[attr-defined]
except ImportError:
    _GenericAlias = type("_GenericAlias", (), {})  # type: ignore[assignment,misc]

_FALSY_VALUES = ["", "0", "n", "no", "false"]
_TRUTHY_VALUES = ["1", "y", "yes", "true"]


def name(type_: type) -> str:
    match = re.match(r"^<class '(.+)'>$", str(type_))
    return match.group(1) if match else str(type_)


def convert(value: str, to: type) -> Union[str, bool, int, float, list, dict, None]:
    if is_optional(to):
        return convert(value, _get_first_optional_subtypes(to))
    if to in [str, int, float]:
        return to(value)
    if to is bool:
        return _to_bool(value)
    if _is_list(to):
        return _to_list(value, to)
    if _is_dict(to):
        return json.loads(value)

    raise ValueError(f"unsupported type for convert(): '{to}'")


def _get_first_optional_subtypes(type_: type) -> type:
    if not is_optional(type_):
        raise ValueError(f"{type_} is not optional (Optional[T] or Union[T, U, ..., None]")

    subtype = first(lambda t: not _is_none_type(t), get_args(type_))
    if subtype is None:
        raise ValueError(f"{type_} is NoneType")
    return subtype


def is_optional(type_: type) -> bool:
    return get_origin(type_) == Union and any(_is_none_type(t) for t in get_args(type_))


def _is_none_type(val: Any) -> bool:
    return isinstance(val, type) and not isinstance(val, _GenericAlias) and isinstance(None, val)


def _is_list(type_: type) -> bool:
    return type_ is list or _is_generic_alias_list(type_)


def _is_generic_alias_list(type_: type) -> bool:
    return get_origin(type_) is list


def _is_dict(type_: type) -> bool:
    return type_ is dict or _is_generic_alias_dict_without_subscription(type_)


def _is_generic_alias_dict_without_subscription(type_: type) -> bool:
    return get_origin(type_) is dict and get_args(type_) == ()


def _to_list(value: str, value_type: type) -> List[Union[str, bool, int, float]]:
    type_args: Final[tuple] = get_args(value_type)
    generic_type: Final[type] = type_args[0] if type_args else str
    return list(value.split(",")) if generic_type is str else [generic_type(element) for element in value.split(",")]


def _to_bool(value: str) -> bool:
    falsy = value.lower() in _FALSY_VALUES
    truthy = value.lower() in _TRUTHY_VALUES
    if falsy is truthy is False:
        raise ValueError(
            f"could not convert string to bool: '{value}'. "
            f"truthy values: {_TRUTHY_VALUES}, falsy values: {_FALSY_VALUES}"
        )
    return truthy

import json
from typing import Protocol, TypeVar, Any, get_args, get_origin, List, Final, Type
from typing import Union

from .functional import first

try:
    # list[T], dict[T,U] etc. python 38 compatibility
    from types import GenericAlias as _GenericAlias  # type: ignore[attr-defined]
except ImportError:
    _GenericAlias = type("_GenericAlias", (), {})  # type: ignore[assignment,misc]

T = TypeVar("T")


class ConverterProtocol(Protocol):
    @staticmethod
    def can_convert(value_type: type) -> bool:
        ...

    @staticmethod
    def convert(value: str, value_type: type) -> Any:
        ...


def get_default_converters_list() -> List[Type["ConverterProtocol"]]:
    return [
        (simple_converter_factory(str)),
        (simple_converter_factory(int)),
        (simple_converter_factory(float)),
        BoolConverter,
        ListConverter,
        DictConverter,
    ]


def simple_converter_factory(type_: type) -> Type[ConverterProtocol]:
    class SimpleConverter(ConverterProtocol):
        __type_name__ = type_.__name__

        @staticmethod
        def can_convert(value_type: type) -> bool:
            return type_ is value_type

        @staticmethod
        def convert(value: str, value_type: type) -> Any:
            return type_(value)

    return SimpleConverter


class BoolConverter(ConverterProtocol):
    _FALSY_VALUES = ["", "0", "n", "no", "false"]
    _TRUTHY_VALUES = ["1", "y", "yes", "true"]

    @staticmethod
    def can_convert(value_type: type) -> bool:
        return value_type is bool

    @staticmethod
    def convert(value: str, value_type: type) -> Any:
        falsy = value.lower() in BoolConverter._FALSY_VALUES
        truthy = value.lower() in BoolConverter._TRUTHY_VALUES
        if falsy is truthy is False:
            raise ValueError(
                f"could not convert string to bool: '{value}'. "
                f"truthy values: {BoolConverter._TRUTHY_VALUES}, falsy values: {BoolConverter._FALSY_VALUES}"
            )
        return truthy


class DictConverter(ConverterProtocol):
    @staticmethod
    def can_convert(value_type: type) -> bool:
        return value_type is dict or DictConverter._is_generic_alias_dict_without_subscription(value_type)

    @staticmethod
    def convert(value: str, value_type: type) -> Any:
        return json.loads(value)

    @staticmethod
    def _is_generic_alias_dict_without_subscription(type_: type) -> bool:
        return get_origin(type_) is dict and get_args(type_) == ()


class ListConverter(ConverterProtocol):
    @staticmethod
    def can_convert(value_type: type) -> bool:
        return value_type is list or ListConverter._is_generic_alias_list(value_type)

    @staticmethod
    def convert(value: str, value_type: type) -> Any:
        type_args: Final[tuple] = get_args(value_type)
        generic_type: Final[type] = type_args[0] if type_args else str
        split = value.split(",")
        return split if generic_type is str else [generic_type(element) for element in split]

    @staticmethod
    def _is_generic_alias_list(type_: type) -> bool:
        return get_origin(type_) is list


class Converter(ConverterProtocol):
    converters_list: List[Type[ConverterProtocol]] = get_default_converters_list()

    @staticmethod
    def register_converter(converter: Type[ConverterProtocol]) -> None:
        Converter.converters_list.append(converter)

    @staticmethod
    def can_convert(_: type) -> bool:
        raise NotImplemented

    @staticmethod
    def convert(value: str, value_type: type) -> Any:
        if Converter._is_optional(value_type):
            return Converter.convert(value, Converter._get_first_optional_subtypes(value_type))
        for converter in Converter.converters_list:
            if converter.can_convert(value_type):
                return converter.convert(value, value_type)

        raise ValueError(f"unsupported type for convert(): '{value_type}'")

    @staticmethod
    def _get_first_optional_subtypes(type_: type) -> type:
        if not Converter._is_optional(type_):
            raise ValueError(f"{type_} is not optional (Optional[T] or Union[T, U, ..., None]")

        subtype = first(lambda t: not Converter._is_none_type(t), get_args(type_))
        if subtype is None:
            raise ValueError(f"{type_} is NoneType")
        return subtype

    @staticmethod
    def _is_optional(type_: type) -> bool:
        return get_origin(type_) == Union and any(Converter._is_none_type(t) for t in get_args(type_))

    @staticmethod
    def _is_none_type(val: Any) -> bool:
        return isinstance(val, type) and not isinstance(val, _GenericAlias) and isinstance(None, val)

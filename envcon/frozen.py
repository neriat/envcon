import types
from typing import Any, NoReturn

from .utils.functional import first

_getattr = object.__getattribute__


class _AccessBaseClassAttributesIfBaseAndDerivedShareSameNameMeta(type):
    def __getattribute__(self, name: str) -> Any:
        self_name = _getattr(self, "__name__")
        bases = _getattr(self, "__bases__")
        base = first(lambda b: _getattr(b, "__name__") == self_name, bases)
        return _getattr(base, name) if base else _getattr(self, name)


class _FrozenInstanceAttributesBase:
    def __setattr__(self, name: str, value: Any) -> NoReturn:
        raise FrozenError()

    def __delattr__(self, name: str) -> NoReturn:
        raise FrozenError()


class _FrozenClassAttributesMeta(
    _FrozenInstanceAttributesBase,
    _AccessBaseClassAttributesIfBaseAndDerivedShareSameNameMeta,
):
    pass


class FrozenError(AttributeError):
    def __init__(self, *args: object) -> None:
        super().__init__("Object is frozen. modifying attributes is not allowed", *args)


def create_frozen_class_from_another_class(cls: type) -> type:

    return types.new_class(
        cls.__name__,
        (cls, _FrozenInstanceAttributesBase),
        kwds={"metaclass": _FrozenClassAttributesMeta},
    )

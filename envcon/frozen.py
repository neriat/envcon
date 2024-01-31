import types
from dataclasses import FrozenInstanceError
from typing import Any, NoReturn


class _FrozenInstanceAttributesBase:
    def __setattr__(self, name: str, value: Any) -> NoReturn:
        raise FrozenInstanceError()

    def __delattr__(self, name: str) -> NoReturn:
        raise FrozenInstanceError()


class _FrozenClassAttributesMeta(_FrozenInstanceAttributesBase, type):
    pass


def create_frozen_class_from_another_class(cls: type) -> type:
    return types.new_class(
        cls.__name__,
        (cls, _FrozenInstanceAttributesBase),
        kwds={"metaclass": _FrozenClassAttributesMeta},
    )

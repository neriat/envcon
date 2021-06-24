import types
from typing import Any, NoReturn


class _DirectAccessToBaseClassAttributesMeta(type):
    def __getattribute__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "__base__"), name)


class _FrozenClassAttributesMeta(_DirectAccessToBaseClassAttributesMeta):
    def __setattr__(self, name: str, value: Any) -> NoReturn:
        raise FrozenError()

    def __delattr__(self, name: str) -> NoReturn:
        raise FrozenError()


class FrozenError(AttributeError):
    def __init__(self, *args: object) -> None:
        super().__init__("Object is frozen. modifying attributes is not allowed", *args)


def create_frozen_class_from_another_class(cls: type) -> type:
    def raise_frozen_error(*_args: Any) -> NoReturn:
        raise FrozenError()

    return types.new_class(
        cls.__name__,
        (cls,),
        kwds={"metaclass": _FrozenClassAttributesMeta},
        exec_body=lambda ns: ns.update({"__setattr__": raise_frozen_error, "__delattr__": raise_frozen_error}),
    )

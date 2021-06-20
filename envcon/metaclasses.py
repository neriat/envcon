from typing import Any, NoReturn, List


class FrozenClassAttributesMeta(type):
    def __setattr__(self, name: str, value: Any) -> NoReturn:
        raise FrozenError()

    def __delattr__(self, name: str) -> NoReturn:
        raise FrozenError()


class DirectAccessToBaseClassAttributesMeta(type):
    def __getattribute__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "__base__"), name)


class InjectedConfigurationClassMeta(FrozenClassAttributesMeta, DirectAccessToBaseClassAttributesMeta):
    pass


class FrozenError(AttributeError):
    def __init__(self, *args: object) -> None:
        super().__init__("Object is frozen. modifying attributes is not allowed", *args)


def frozen_class_instance_exec_body(namespace: dict) -> None:
    def raise_frozen_error(*_args: Any) -> NoReturn:
        raise FrozenError()

    namespace.update({"__setattr__": raise_frozen_error, "__delattr__": raise_frozen_error})

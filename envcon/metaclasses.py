from typing import Any, NoReturn


class FrozenClassAttributesMeta(type):
    def __setattr__(self, name: str, value: Any) -> NoReturn:
        raise FrozenClassAttributesError()

    def __delattr__(self, name: str) -> NoReturn:
        raise FrozenClassAttributesError()


class DirectAccessToBaseClassAttributesMeta(type):
    def __getattribute__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "__base__"), name)


class InjectedConfigurationClassMeta(FrozenClassAttributesMeta, DirectAccessToBaseClassAttributesMeta):
    pass


class FrozenClassAttributesError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__("Class is frozen. modifying attributes is not allowed", *args)

import typing
from typing import Callable, Union, Mapping, TypeVar, Type, Optional, overload, TypeAlias

from .configuration_injector import ConfigurationInjector
from .extended_environ import ExtendedEnviron

T = TypeVar("T")
Class: TypeAlias = Union[type, Type[T], T]  # type for mypy, Type[T] for pycharm 2023.3.2


def configuration(
    *,
    prefix: str,
    source: Mapping[str, str],
) -> Callable[[Type[T]], T]:
    def wrap(cls: Type[T]) -> T:
        # this cast is necessary for code-assistant and has no effect
        return typing.cast(T, ConfigurationInjector(cls, prefix, source).process_class())

    return wrap


@overload
def environment_configuration(
    *,
    prefix: str = "",
    dot_env_path: Optional[str] = ".env",
) -> Callable[[Class], T]:
    ...


@overload
def environment_configuration(cls: Class) -> Class:
    ...


def environment_configuration(
    cls: Optional[Class] = None,
    *,
    prefix: str = "",
    dot_env_path: Optional[str] = ".env",
) -> Union[Class, Callable[[Type[T]], T]]:
    wrap = configuration(
        prefix=prefix,
        source=ExtendedEnviron(dot_env_path),
    )
    return wrap if cls is None else wrap(cls)

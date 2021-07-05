from typing import Callable, Union, Mapping, TypeVar, Type, Optional

from .configuration_injector import ConfigurationInjector
from .extended_environ import ExtendedEnviron

T = TypeVar("T")
Class = Union[type, Type[T]]  # type for mypy, Type[T] for pycharm 2021.1.1


def configuration(*, prefix: str, source: Mapping[str, str], frozen: bool = True) -> Callable[[type], type]:
    def wrap(cls: type) -> type:
        return ConfigurationInjector(cls, prefix, source, frozen).process_class()

    return wrap


def environment_configuration(
    cls: Optional[Class] = None, *, prefix: str = "", include_dot_env_file: bool = True, frozen: bool = True
) -> Union[Class, Callable[[Class], Class]]:
    wrap = configuration(prefix=prefix, source=ExtendedEnviron(include_dot_env_file), frozen=frozen)
    return wrap if cls is None else wrap(cls)

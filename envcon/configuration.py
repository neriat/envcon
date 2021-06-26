from typing import Callable, Union, Mapping, TypeVar, Type, Optional

from .configuration_injector import _ConfigurationInjector
from .extended_environ import ExtendedEnviron

T = TypeVar("T")
Class = Union[type, Type[T]]  # type for mypy, Type[T] for pycharm 2021.1.1


def configuration(*, prefix: str, source: Mapping[str, str], frozen: bool = True) -> Callable[[type], type]:
    return lambda cls: _ConfigurationInjector.inject_class(cls, prefix, source, frozen)


def environment_configuration(
    target_class: Optional[Class] = None, *, prefix: str = "", include_dot_env_file: bool = True, frozen: bool = True
) -> Union[Class, Callable[[Class], Class]]:
    source = ExtendedEnviron(include_dot_env_file)
    if target_class:  # decorator used without parentheses
        return configuration(prefix=prefix, source=source, frozen=frozen)(target_class)
    else:
        return configuration(prefix=prefix, source=source, frozen=frozen)

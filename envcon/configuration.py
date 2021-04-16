from typing import Callable, Union, Mapping

from .configuration_injector import _ConfigurationInjector
from .extended_environ import ExtendedEnviron


def configuration(*, prefix: str, source: Mapping[str, str]) -> Callable[[type], type]:
    return lambda cls: _ConfigurationInjector.inject_class(cls, prefix, source)


def environment_configuration(
    target_class: type = None, *, prefix: str = "", include_dot_env_file: bool = True
) -> Union[Callable[[type], type], type]:

    source = ExtendedEnviron(include_dot_env_file)
    if target_class:  # decorator used without parentheses
        return configuration(prefix=prefix, source=source)(target_class)
    else:
        return configuration(prefix=prefix, source=source)

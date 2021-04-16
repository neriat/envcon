from typing import get_type_hints, Mapping, Union, Optional, Any

from .extended_environ import ExtendedEnviron
from .utils import type_utils, inspections


class _ConfigurationInjector:
    def __init__(self, target_class: type, prefix: str, source: Mapping[str, str]) -> None:
        self.target_class = target_class
        self.prefix = prefix
        self.source = source

    @staticmethod
    def inject_class(target_class: type, prefix: str, source: Mapping[str, str]) -> type:
        injector = _ConfigurationInjector(target_class, prefix, source)
        injector._inject_target_class()
        return injector.target_class

    def _inject_target_class(self) -> None:
        for variable_name, variable_type in get_type_hints(self.target_class).items():
            value = self._get_variable_value(variable_name, variable_type)
            setattr(self.target_class, variable_name, value)

    def _get_variable_value(self, var_name: str, var_type: type) -> Union[str, bool, int, float, list, dict, None]:
        default_value = self._get_default_value(var_name)
        lookup_key = self.prefix + var_name
        value = self.source.get(lookup_key, None)
        if value is None and default_value is None and not type_utils.is_optional(var_type):
            raise LookupError(self._missing_variable_error_message(lookup_key))
        try:
            return type_utils.convert(value, var_type) if value is not None else default_value
        except ValueError as e:
            raise ValueError(f"couldn't convert {var_name} to {type_utils.name(var_type)}. {e}") from None

    def _get_default_value(self, var_name: str) -> Optional[Any]:
        return getattr(self.target_class, var_name, None)

    def _missing_variable_error_message(self, lookup_key: str) -> str:
        if isinstance(self.source, ExtendedEnviron):
            return f"{lookup_key} is not an environment variable, nor has default value"
        else:
            source_name = inspections.retrieve_name(self.source) or "your source"
            return f"{lookup_key} does not exist in {source_name}, nor has default value"

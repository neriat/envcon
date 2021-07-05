from typing import get_type_hints, Mapping, Union, Any, NoReturn

from .extended_environ import ExtendedEnviron
from .frozen import create_frozen_class_from_another_class
from .utils import type_utils, inspections


class ConfigurationInjector:
    def __init__(self, target_class: type, prefix: str, source: Mapping[str, str], frozen: bool) -> None:
        self.target_class = target_class
        self.prefix = prefix
        self.source = source
        self.frozen = frozen

    def process_class(self) -> type:
        for variable_name, variable_type in get_type_hints(self.target_class).items():
            value = self._get_variable_value(variable_name, variable_type)
            self._set_attribute_in_target_class(variable_name, value)
        return self.target_class if not self.frozen else create_frozen_class_from_another_class(self.target_class)

    def _set_attribute_in_target_class(self, name: str, value: Any) -> None:
        # why not directly call setattr?
        # because we need to skip _FrozenClassAttributesMeta restrictions if presented any in case of inheritance
        type.__setattr__(self.target_class, name, value)

    def _get_variable_value(self, var_name: str, var_type: type) -> Union[str, bool, int, float, list, dict, None]:
        default_value = getattr(self.target_class, var_name, None)
        lookup_key = self.prefix + var_name
        value = self.source.get(lookup_key, None)
        if value is None and default_value is None and not type_utils.is_optional(var_type):
            self._raise_missing_variable(var_name, lookup_key)
        try:
            return default_value if value is None else type_utils.convert(value, var_type)
        except ValueError as e:
            raise ValueError(f"couldn't convert {var_name} to {type_utils.name(var_type)}. {e}") from None

    def _raise_missing_variable(self, var_name: str, lookup_key: str) -> NoReturn:
        if isinstance(self.source, ExtendedEnviron):
            raise LookupError(
                f"{lookup_key} is not an environment variable, nor has default value"
                if var_name == lookup_key
                else f"{lookup_key} is not an environment variable, nor {var_name} has default value"
            )
        raise LookupError(
            f"{lookup_key} does not exist in {self._get_source_name()}, nor has default value"
            if var_name == lookup_key
            else f"{lookup_key} does not exist in {self._get_source_name()}, nor {var_name} has default value"
        )

    def _get_source_name(self) -> str:
        return inspections.retrieve_name(self.source) or "your source"

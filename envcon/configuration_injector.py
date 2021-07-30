from typing import TypeVar
from typing import get_type_hints, Mapping, Union, Any, NoReturn, Dict, Callable

from .extended_environ import ExtendedEnviron
from .frozen import create_frozen_class_from_another_class
from .utils import type_utils, inspections

Self = TypeVar("Self")


class ConfigurationInjector:
    def __init__(
        self,
        target_class: type,
        prefix: str,
        source: Mapping[str, str],
        frozen: bool,
        override_init: bool,
        override_repr: bool,
    ) -> None:
        self.target_class = target_class
        self.prefix = prefix
        self.source = source
        self.frozen = frozen
        self.override_init = override_init
        self.override_repr = override_repr

        self._target_class_variables_injected_values = self._get_all_variables_values()

    def process_class(self) -> type:
        if self.override_init:
            self._set_attribute_in_target_class("__init__", self._create_init_function())

        if self.override_repr:
            self._set_attribute_in_target_class("__repr__", self._create_repr_function())

        for variable_name, value in self._target_class_variables_injected_values.items():
            self._set_attribute_in_target_class(variable_name, value)

        return self.target_class if not self.frozen else create_frozen_class_from_another_class(self.target_class)

    @staticmethod
    def _create_init_function() -> Callable[[Self], None]:
        def __init__(self: Self) -> None:
            pass

        return __init__

    def _create_repr_function(self) -> Callable[[Self], str]:
        class_name = self.target_class.__qualname__
        variables_names = self._target_class_variables_injected_values.keys()

        def __repr__(self: Self) -> str:
            comma_separated_values = ",".join(
                f"{var_name}={getattr(self, var_name)}"
                for var_name in filter(lambda var_name: hasattr(self, var_name), variables_names)
            )
            return f"{class_name}({comma_separated_values})"

        return __repr__

    def _set_attribute_in_target_class(self, name: str, value: Any) -> None:
        # why not directly call setattr?
        # because we need to skip _FrozenClassAttributesMeta restrictions if presented any in case of inheritance
        type.__setattr__(self.target_class, name, value)

    def _get_all_variables_values(self) -> Dict[str, Union[str, bool, int, float, list, dict, None]]:
        return {
            variable_name: self._get_variable_value(variable_name, variable_type)
            for variable_name, variable_type in get_type_hints(self.target_class).items()
        }

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
                f"'{lookup_key}' is not an environment variable, nor has default value"
                if var_name == lookup_key
                else f"'{lookup_key}' is not an environment variable, nor '{var_name}' has default value"
            )
        raise LookupError(
            f"'{lookup_key}' does not exist in {self._get_source_name()}, nor has default value"
            if var_name == lookup_key
            else f"'{lookup_key}' does not exist in {self._get_source_name()}, nor '{var_name}' has default value"
        )

    def _get_source_name(self) -> str:
        return inspections.retrieve_name(self.source) or "your source"

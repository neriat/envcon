from .configuration import environment_configuration, configuration
from dataclasses import FrozenInstanceError

FrozenError = FrozenInstanceError  # compat. will be removed next major

__all__ = ["environment_configuration", "configuration", "FrozenError"]

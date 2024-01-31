import os
from typing import Mapping, Iterator, NoReturn, Any, Optional, Dict

import dotenv


class ExtendedEnviron(Mapping[str, str]):
    def __init__(self, dot_env_path: Optional[str]) -> None:
        self._dot_env: Dict[str, Optional[str]] = dotenv.dotenv_values(dot_env_path) if dot_env_path is not None else {}

    def __getitem__(self, key: str) -> str:
        if not isinstance(key, str):
            raise ValueError(f"str expected, not {type(key)}")

        try:
            return self._environ[key]
        except KeyError:
            raise KeyError(key) from None

    def __setitem__(self, key: Any, value: Any) -> NoReturn:
        raise NotImplementedError("object is readonly. set is not allowed")

    def __len__(self) -> int:
        return len(self._environ)

    def __iter__(self) -> Iterator[str]:
        return iter(self._environ)

    @property
    def _environ(self) -> Mapping:
        return {**self._dot_env, **os.environ} if self._dot_env else os.environ

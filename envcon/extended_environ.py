import os
from typing import Mapping, Iterator, NoReturn, Any, Optional, Dict

import dotenv


class ExtendedEnviron(Mapping[str, str]):
    def __init__(self, read_dot_env_file: bool) -> None:
        self._dot_env: Dict[str, Optional[str]] = dotenv.dotenv_values(".env") if read_dot_env_file else {}

    def __getitem__(self, key: str) -> str:
        if not isinstance(key, str):
            raise ValueError(f"str expected, not {type(key)}")

        try:
            return self.get_dot_env_combined_with_environ()[key]
        except KeyError:
            raise KeyError(key) from None

    def __setitem__(self, key: Any, value: Any) -> NoReturn:
        raise NotImplementedError("object is readonly. set is not allowed")

    def __len__(self) -> int:
        return len(self.get_dot_env_combined_with_environ())

    def __iter__(self) -> Iterator[str]:
        return iter(self.get_dot_env_combined_with_environ())

    def get_dot_env_combined_with_environ(self) -> Mapping:
        return {**self._dot_env, **os.environ} if self._dot_env else os.environ

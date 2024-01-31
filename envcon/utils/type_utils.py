import re
from typing import Union

from .converter import Converter


def name(type_: type) -> str:
    match = re.match(r"^<class '(.+)'>$", str(type_))
    return match.group(1) if match else str(type_)


def convert(value: str, to: type) -> Union[str, bool, int, float, list, dict, None]:
    return Converter.convert(value, to)

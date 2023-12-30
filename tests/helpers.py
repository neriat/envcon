import sys
from typing import Callable

import pytest

is_python_38: bool = sys.version_info[:2] < (3, 9)

skip_if_python38_is_presented = pytest.mark.skipif(
    is_python_38,
    reason=(
        f"list and dict are not subscriptable on earlier python versions. "
        f"your version: {'.'.join(str(i) for i in (sys.version_info[:3]))}, required: >=3.9"
    ),
)

sample_configuration: dict = {
    "SOME_A": "value_a",
    "SOME_B": "value_b",
    "SOME_INT": "42",
    "LIST_STRING": "a,b,c",
    "LIST_INTEGERS": "420, 69",
    "DICT_ENV": '{"key": "value", "a":42}',
    "DICT_MULTILEVEL": '{"key": [{"a":42},{"a":4.2},{"a":"42"}]}',
    "ZXC_SOME_A": "prefixed_a",
    "ZXC_SOME_B": "prefixed_a",
}


def not_test(func: Callable) -> Callable:
    """
    pytest 7 assume any function is a test, this is not always the case
    """
    func.__test__ = False  # type: ignore[attr-defined]
    return func

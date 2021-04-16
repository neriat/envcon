from typing import List

import pytest
from envcon import configuration

from shared import configuration_sample


def test_empty_configuration_class():
    @configuration(prefix="", source=configuration_sample)
    class Test:
        pass


def test_simple_injection():
    @configuration(prefix="", source=configuration_sample)
    class Test:
        SOME_A: str
        SOME_B: str
        SOME_INT: int

    assert Test.SOME_A == "value_a"
    assert Test.SOME_B == "value_b"
    assert Test.SOME_INT == 42


def test_missing_field():
    with pytest.raises(LookupError):

        @configuration(prefix="", source=configuration_sample)
        class Test:
            SOME_A: str
            NOT_EXIST: List[int]

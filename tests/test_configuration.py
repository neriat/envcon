from typing import List

import pytest
from envcon import configuration, FrozenClassAttributesError

from utils import sample_configuration


def test_empty_configuration_class():
    @configuration(prefix="", source=sample_configuration)
    class Test:
        pass


def test_simple_injection():
    @configuration(prefix="", source=sample_configuration)
    class Test:
        SOME_A: str
        SOME_B: str
        SOME_INT: int

    assert Test.SOME_A == "value_a"
    assert Test.SOME_B == "value_b"
    assert Test.SOME_INT == 42


def test_missing_field():
    with pytest.raises(LookupError):

        @configuration(prefix="", source=sample_configuration)
        class Test:
            SOME_A: str
            NOT_EXIST: List[int]


def test_set_frozen_attribute_in_frozen_class():
    @configuration(prefix="", source=sample_configuration, frozen=True)
    class Test:
        SOME_A: str

    with pytest.raises(FrozenClassAttributesError):
        Test.SOME_A = "should fail"


def test_delete_frozen_attribute_in_frozen_class():
    @configuration(prefix="", source=sample_configuration, frozen=True)
    class Test:
        SOME_A: str

    with pytest.raises(FrozenClassAttributesError):
        del Test.SOME_A


def test_set_frozen_attribute_in_unfrozen_class():
    @configuration(prefix="", source=sample_configuration, frozen=False)
    class Test:
        SOME_A: str

    Test.SOME_A = "should not fail"
    assert Test.SOME_A == "should not fail"


def test_delete_frozen_attribute_in_unfrozen_class():
    @configuration(prefix="", source=sample_configuration, frozen=False)
    class Test:
        SOME_A: str

    del Test.SOME_A
    assert not hasattr(Test, "SOME_A")

from typing import List

import pytest
from envcon import configuration, FrozenError

from helpers import sample_configuration


def test_empty_configuration_class() -> None:
    @configuration(prefix="", source=sample_configuration)
    class Test:
        pass


def test_simple_injection() -> None:
    @configuration(prefix="", source=sample_configuration)
    class Test:
        SOME_A: str
        SOME_B: str
        SOME_INT: int

    assert Test.SOME_A == "value_a"
    assert Test.SOME_B == "value_b"
    assert Test.SOME_INT == 42


def test_missing_field() -> None:
    with pytest.raises(LookupError):

        @configuration(prefix="", source=sample_configuration)
        class Test:
            SOME_A: str
            NOT_EXIST: List[int]


def test_set_attribute_in_frozen_class() -> None:
    @configuration(prefix="", source=sample_configuration, frozen=True)
    class Test:
        SOME_A: str

    with pytest.raises(FrozenError):
        Test.SOME_A = "should fail"


def test_delete_attribute_in_frozen_class() -> None:
    @configuration(prefix="", source=sample_configuration, frozen=True)
    class Test:
        SOME_A: str

    with pytest.raises(FrozenError):
        del Test.SOME_A


def test_set_attribute_in_frozen_class_instance() -> None:
    @configuration(prefix="", source=sample_configuration, frozen=True)
    class Test:
        SOME_A: str

    t = Test()
    with pytest.raises(FrozenError):
        t.SOME_A = "should fail"


def test_delete_attribute_in_frozen_class_instance() -> None:
    @configuration(prefix="", source=sample_configuration, frozen=True)
    class Test:
        SOME_A: str

    t = Test()
    with pytest.raises(FrozenError):
        del t.SOME_A


def test_set_attribute_in_unfrozen_class() -> None:
    @configuration(prefix="", source=sample_configuration, frozen=False)
    class Test:
        SOME_A: str

    Test.SOME_A = "should not fail"
    assert Test.SOME_A == "should not fail"


def test_delete_attribute_in_unfrozen_class() -> None:
    @configuration(prefix="", source=sample_configuration, frozen=False)
    class Test:
        SOME_A: str

    del Test.SOME_A
    assert not hasattr(Test, "SOME_A")


def test_set_attribute_in_unfrozen_class_instance() -> None:
    @configuration(prefix="", source=sample_configuration, frozen=False)
    class Test:
        SOME_A: str

    t = Test()
    t.SOME_A = "should not fail"
    assert t.SOME_A == "should not fail"


def test_delete_attribute_in_unfrozen_class_instance() -> None:
    @configuration(prefix="", source=sample_configuration, frozen=False, override_init=False)
    class Test:
        SOME_A: str

        def __init__(self) -> None:
            self.SOME_B = "some_b"

    t = Test()
    del t.SOME_B
    assert not hasattr(t, "SOME_B")

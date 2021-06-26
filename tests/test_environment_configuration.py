import os
from typing import List, Dict, Generator
import itertools

import pytest

from envcon import environment_configuration
from helpers import sample_configuration, skip_if_python38_is_presented


@pytest.fixture(scope="module", autouse=True)
def patch_environ() -> Generator:
    os_environ_dump = os.environ
    os.environ = sample_configuration  # type: ignore[assignment]
    yield
    os.environ = os_environ_dump


def test_empty_configuration_class() -> None:
    @environment_configuration
    class Test:
        pass


def test_empty_configuration_class_with_parentheses() -> None:
    @environment_configuration()
    class Test:
        pass


def test_simple_injection() -> None:
    @environment_configuration
    class Test:
        SOME_A: str
        SOME_B: str
        SOME_INT: int

    assert Test.SOME_A == "value_a"
    assert Test.SOME_B == "value_b"
    assert Test.SOME_INT == 42


def test_simple_injection_with_parentheses() -> None:
    @environment_configuration()
    class Test:
        SOME_A: str
        SOME_B: str
        SOME_INT: int

    assert Test.SOME_A == "value_a"
    assert Test.SOME_B == "value_b"
    assert Test.SOME_INT == 42


def test_simple_list_injection() -> None:
    @environment_configuration
    class Test:
        LIST_STRING: list

    assert Test.LIST_STRING == ["a", "b", "c"]


@skip_if_python38_is_presented
def test_list_injection39() -> None:
    @environment_configuration
    class Test:
        LIST_INTEGERS: list[int]  # type: ignore[misc]

    assert Test.LIST_INTEGERS == [420, 69]


def test_list_from_typing_injection() -> None:
    @environment_configuration
    class Test:
        LIST_STRING: List
        LIST_INTEGERS: List[int]

    assert Test.LIST_STRING == ["a", "b", "c"]
    assert Test.LIST_INTEGERS == [420, 69]


def test_missing_field() -> None:
    with pytest.raises(LookupError):

        @environment_configuration
        class Test:
            SOME_A: str
            NOT_EXIST: List[int]


def test_missing_field_but_has_default_value() -> None:
    @environment_configuration
    class Test:
        SOME_A: str
        NOT_EXIST: List[int] = [1, 2]


def test_cast_int_error() -> None:
    with pytest.raises(ValueError):

        @environment_configuration
        class Test:
            SOME_A: int


def test_cast_list_error() -> None:
    with pytest.raises(ValueError):

        @environment_configuration
        class Test:
            LIST_STRING: List[int]


def test_dict_injection() -> None:
    @environment_configuration
    class Test:
        DICT_ENV: dict

    assert len(Test.DICT_ENV) == 2
    assert Test.DICT_ENV["key"] == "value"
    assert Test.DICT_ENV["a"] == 42


def test_dict_from_type_injection() -> None:
    @environment_configuration
    class Test:
        DICT_ENV: Dict

    assert len(Test.DICT_ENV) == 2
    assert Test.DICT_ENV["key"] == "value"
    assert Test.DICT_ENV["a"] == 42


def test_multilevel_dict_injection() -> None:
    @environment_configuration
    class Test:
        DICT_MULTILEVEL: dict

    assert len(Test.DICT_MULTILEVEL) == 1
    arr = Test.DICT_MULTILEVEL["key"]
    assert len(arr) == 3
    assert arr[0]["a"] == 42
    assert arr[1]["a"] == 4.2
    assert arr[2]["a"] == "42"


def test_injection_with_prefix() -> None:
    @environment_configuration(prefix="SOME_")
    class Test:
        A: str
        B: str
        INT: int

    assert Test.A == "value_a"
    assert Test.B == "value_b"
    assert Test.INT == 42

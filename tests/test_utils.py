from typing import Optional, Union, List, Dict, Callable, Sequence, TypeVar

import pytest

from envcon.utils import type_utils, inspections, functional
from shared import IS_PYTHON38, PYTHON38_SKIP_MESSAGE

T = TypeVar("T")


@pytest.mark.parametrize(
    "type_, expected",
    [
        (Optional[str], True),
        (Optional[List], True),
        (Optional[dict], True),
        (Optional[Dict[str, int]], True),
        (Union[int, None], True),
        (Union[None, int], True),
        (Optional[Union[str, int]], True),
        (Union[Optional[str]], True),
        (Union[Optional[str], int], True),
        (List[Optional[str]], False),
        (Union[str, int], False),
        (Dict[None, int], False),
        (Dict[str, None], False),
    ],
)
def test_is_optional(type_: type, expected: bool):
    assert type_utils.is_optional(type_) == expected


# noinspection PyTypeHints
@pytest.mark.skipif(
    IS_PYTHON38,
    reason=PYTHON38_SKIP_MESSAGE,
)
@pytest.mark.parametrize(
    "type_, expected",
    [
        (Optional[dict[str, int]], True),
        (list[Optional[str]], False),
        (dict[None, int], False),
        (dict[str, None], False),
    ],
)
def test_is_optional39(type_: type, expected: bool):
    assert type_utils.is_optional(type_) == expected


@pytest.mark.parametrize(
    "type_, expected",
    [
        (list, True),
        (List, True),
        (List[str], True),
        (List[dict], True),
        (Optional[List], False),
        (Optional[List[int]], False),
        (Optional[list], False),
        (dict, False),
        (Dict, False),
        (Dict[list, str], False),
        (Dict[List, list], False),
    ],
)
def test_is_list(type_: type, expected: bool):
    assert type_utils._is_list(type_) == expected


# noinspection PyTypeHints
@pytest.mark.skipif(
    IS_PYTHON38,
    reason=PYTHON38_SKIP_MESSAGE,
)
@pytest.mark.parametrize(
    "type_, expected",
    [
        (list[str], True),
        (list[dict], True),
        (Optional[list[int]], False),
        (dict[list, str], False),
    ],
)
def test_is_list39(type_: type, expected: bool):
    assert type_utils._is_list(type_) == expected


def test_retrieve_name():
    vari = "some"
    able = "value"
    a = {}
    b = {}
    c = dict()
    d = dict()

    assert inspections.retrieve_name(vari) == "vari"
    assert inspections.retrieve_name(able) == "able"
    assert inspections.retrieve_name(a) == "a"
    assert inspections.retrieve_name(b) == "b"
    assert inspections.retrieve_name(c) == "c"
    assert inspections.retrieve_name(d) == "d"


@pytest.mark.parametrize(
    "array, predicate, expected",
    [
        ([1, 2, 3, 4], lambda i: i == 2, 2),
        ([1, 2, 3, 4], lambda i: i > 10, None),
        ([1, 2, 3, 4], lambda i: i > 2, 3),
        (["a1", "a2", "aa3", "aaa4"], lambda s: s.startswith("aa"), "aa3"),
    ],
)
def test_first(array: Sequence[T], predicate: Callable[[Sequence[T]], bool], expected: Optional[T]):
    assert functional.first(predicate, array) == expected

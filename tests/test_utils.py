from typing import Optional, Union, List, Dict, Callable, Sequence, TypeVar, Any

import pytest

from envcon.utils import type_utils, inspections, functional, converter
from helpers import skip_if_python38_is_presented, is_python_38

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
def test_is_optional(type_: type, expected: bool) -> None:
    assert type_utils._is_optional(type_) == expected


@skip_if_python38_is_presented
@pytest.mark.parametrize(
    "type_, expected",
    (
        lambda: ()
        if is_python_38
        else (
            (Optional[dict[str, int]], True),  # type: ignore[misc]
            (list[Optional[str]], False),  # type: ignore[misc]
            (dict[None, int], False),  # type: ignore[misc]
            (dict[str, None], False),  # type: ignore[misc]
        )
    )(),
)
def test_is_optional39(type_: type, expected: bool) -> None:
    assert type_utils._is_optional(type_) == expected


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
def test_is_list(type_: type, expected: bool) -> None:
    assert converter.ListConverter.can_convert(type_) == expected


@skip_if_python38_is_presented
@pytest.mark.parametrize(
    "type_, expected",
    (
        lambda: ()
        if is_python_38
        else (
            (list[str], True),  # type: ignore[misc]
            (list[dict], True),  # type: ignore[misc]
            (Optional[list[int]], False),  # type: ignore[misc]
            (dict[list, str], False),  # type: ignore[misc]
        )
    )(),
)
def test_is_list39(type_: type, expected: bool) -> None:
    assert converter.ListConverter.can_convert(type_) == expected


def test_retrieve_name() -> None:
    vari: str = "some"
    able: str = "value"
    a: dict = {}
    b: dict = {}
    c: dict = dict()
    d: dict = dict()

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
def test_first(array: Sequence[T], predicate: Callable[[Optional[T]], Any], expected: Optional[T]) -> None:
    assert functional.first(predicate, array) == expected

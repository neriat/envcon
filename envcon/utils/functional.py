from typing import Callable, Sequence, Optional, TypeVar

T = TypeVar("T")


def first(predicate: Callable[[Sequence], bool], sequence: Sequence[T]) -> Optional[T]:
    return next(filter(predicate, sequence), None)

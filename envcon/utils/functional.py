from typing import Callable, Sequence, Optional, TypeVar, Any

T = TypeVar("T")


def first(predicate: Callable[[Optional[T]], Any], sequence: Sequence[T]) -> Optional[T]:
    return next(filter(predicate, sequence), None)

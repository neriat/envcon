from dataclasses import FrozenInstanceError
from typing import Any, Optional

import pytest

# noinspection PyProtectedMember
from envcon.frozen import (
    _AccessBaseClassAttributesIfBaseAndDerivedShareSameNameMeta,
    _FrozenClassAttributesMeta,
    create_frozen_class_from_another_class,
)
from helpers import not_test


@not_test
def test_freeze_class_parameterization(metaclass: Optional[type] = None) -> tuple:
    Meta: Any = metaclass if metaclass else type

    class EmptyClass(metaclass=Meta):
        pass

    class WithClassAttributes(metaclass=Meta):
        bla: int = 42
        blu: float = 0.42

    return EmptyClass, WithClassAttributes


def test_access_base_class_attributes_if_base_and_subclass_share_same_name_meta() -> None:
    class Bla:
        attr: int = 42

    class Blu(Bla, metaclass=_AccessBaseClassAttributesIfBaseAndDerivedShareSameNameMeta):
        attr: int = 420

    class Bla(Bla, metaclass=_AccessBaseClassAttributesIfBaseAndDerivedShareSameNameMeta):  # type: ignore[no-redef]
        attr: int = 0x420

    assert Blu.attr == 420
    assert Bla.attr == 42
    assert object.__getattribute__(Bla, "attr") == 0x420


@pytest.mark.parametrize("cls", test_freeze_class_parameterization(metaclass=_FrozenClassAttributesMeta))
def test_frozen_class_attributes_meta(cls: type) -> None:
    with pytest.raises(FrozenInstanceError):
        cls.bla = 41  # type: ignore[attr-defined]
    with pytest.raises(FrozenInstanceError):
        del cls.bla  # type: ignore[attr-defined]


@pytest.mark.parametrize("cls", test_freeze_class_parameterization())
def test_create_frozen_class_from_another_class(cls: type) -> None:
    FrozenClass = create_frozen_class_from_another_class(cls)
    t = FrozenClass()
    with pytest.raises(FrozenInstanceError):
        t.bla = 41
    with pytest.raises(FrozenInstanceError):
        del t.blu


def test_freeze_modify_instance_attributes() -> None:
    class WithInstanceAttributes:
        def __init__(self, bla: int = 42) -> None:
            self.bla: int = bla

    FrozenTest = create_frozen_class_from_another_class(WithInstanceAttributes)
    with pytest.raises(FrozenInstanceError):
        FrozenTest()

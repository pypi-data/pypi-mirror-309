"""SingleBooleanComponent class module."""

from .core import BaseComponent
from .core import SingleValueComponent

from .single_boolean_components import SingleBooleanComponent, SimpleToggle


def test_is_single_value_subclass():
    assert issubclass(SingleBooleanComponent, SingleValueComponent)


def test_default_value():
    c = SingleBooleanComponent("id")

    assert not c.value


def test_subclasses():
    assert issubclass(SimpleToggle, SingleBooleanComponent)


def test_gets_registered():
    cid = "id"
    c = SimpleToggle(cid)
    assert BaseComponent.registry.get(cid) == c

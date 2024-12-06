"""SingleBooleanComponent class module."""

from zmc.utils.deprecated import deprecated_component

from .core import SingleValueComponent


__all__ = ["Toggle", "SimpleToggle"]


class SingleBooleanComponent(SingleValueComponent):
    """Boolean receiver class which contains a single value."""

    def __init__(self, component_id):
        super().__init__(component_id, False)


class SimpleToggle(SingleBooleanComponent):
    """Simple Toggle class containing a single boolean value.

    The class has a single boolean value that can be accessed as an attribute:
    `toggle.value`.

    Callbacks will be called with the value as the first and only parameter.
    """


@deprecated_component(version="0.1.0", reason="Use SimpleToggle instead")
class Toggle(SimpleToggle):
    """Toggle class containing a single boolean value.

    The class has a single boolean value that can be accessed as an attribute:
    `toggle.value`.

    Callbacks will be called with the value as the first and only parameter.
    """

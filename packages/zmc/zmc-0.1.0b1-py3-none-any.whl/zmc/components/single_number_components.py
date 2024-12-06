"""SingleNumberComponent class module."""

from zmc.utils.deprecated import deprecated_component

from .core import SingleValueComponent


__all__ = [
    "Slider",
    "VerticalSlider",
    "HorizontalSlider",
    "NumericInput",
    "NumericDropdown",
]


class SingleNumberComponent(SingleValueComponent):
    """Number receiver class which contains a single value."""

    def __init__(self, component_id):
        super().__init__(component_id, 1)


class HorizontalSlider(SingleNumberComponent):
    """Horizontal Slider class which contains a single value.

    A slider has a value of a single number that can be accessed as an
    attribute: `slider.value`.

    Callbacks will be called with the value as the first and only parameter.
    """


class VerticalSlider(SingleNumberComponent):
    """Vertical Slider class which contains a single value.

    A slider has a value of a single number that can be accessed as an
    attribute: `slider.value`.

    Callbacks will be called with the value as the first and only parameter.
    """


@deprecated_component(
    version="0.1.0", reason="Use HorizontalSlider or VerticalSlider instead"
)
class Slider(SingleNumberComponent):
    """Slider class which contains a single value.

    A slider has a value of a single number that can be accessed as an
    attribute: `slider.value`.

    Callbacks will be called with the value as the first and only parameter.
    """


class NumericInput(SingleNumberComponent):
    """Numeric class representing a number input component.

    The class has a single value that can be accessed as an attribute:
    `numeric_input.value`.

    Callbacks will be called with the value as the first and only parameter.
    """


class NumericDropdown(SingleNumberComponent):
    """Numeric class representing a dropdown number component.

    The class has a single value that can be accessed as an attribute:
    `numeric_dropdown.value`.

    Callbacks will be called with the value as the first and only parameter.
    """

"""SingleTextComponent class module."""

from zmc.utils.deprecated import deprecated_component

from .core import SingleValueComponent


__all__ = ["TextInput", "FilepathInput", "FilepathPicker", "TextDropdown"]


class SingleTextComponent(SingleValueComponent):
    """Text receiver class which contains a single value."""

    def __init__(self, component_id):
        super().__init__(component_id, "")


class TextInput(SingleTextComponent):
    """Text class representing a freeform text component.

    The class has a single value that can be accessed as an attribute:
    `text_input.value`.

    Callbacks will be called with the value as the first and only parameter.
    """


class TextDropdown(SingleTextComponent):
    """Text class representing a dropdown text component.

    The class has a single value that can be accessed as an attribute:
    `text_dropdown.value`.

    Callbacks will be called with the value as the first and only parameter.
    """


class FilepathPicker(SingleTextComponent):
    """Filepath class, representing a file path choosen from the app.

    The class has a single value that can be accessed as an attribute:
    `filepath.value`.
    """


@deprecated_component(version="0.1.0", reason="Use FilepathPicker instead")
class FilepathInput(FilepathPicker):
    """Filepath class, representing a file path choosen from the app.

    The class has a single value that can be accessed as an attribute:
    `filepath.value`.
    """

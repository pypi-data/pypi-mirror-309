"""ButtonComponent class module."""

from zmc.utils.deprecated import deprecated_component

from .core import ValueReceiverBaseComponent


__all__ = ["Button", "SimpleButton"]


class SimpleButton(ValueReceiverBaseComponent):
    """Button class that calls one or more functions whenever it is clicked.

    The function(s) will be called with no arguments.
    """

    # No value but this is still needed to make the class concrete.
    def _set_value(self, _):
        """No value is set for buttons"""

    def _callback_args(self):
        return []


@deprecated_component(version="0.1.0", reason="Use SimpleButton instead")
class Button(SimpleButton):
    """Button class that calls one or more functions whenever it is clicked.

    The function(s) will be called with no arguments.
    """

"""Graph class module."""

from zmc.utils.deprecated import deprecated_component

from .core import DataSenderBaseComponent


__all__ = ["Graph", "LineGraph"]


class LineGraph(DataSenderBaseComponent):
    """Line Graph component class."""

    def __init__(self, component_id):
        super().__init__(component_id)
        self._x = []
        self._y = []

    @property
    def data(self):
        return {
            "lines": [
                {
                    "x": list(self._x),
                    "y": list(self._y),
                }
            ]
        }

    def append_data(self, x, y):
        """Add a x, y pair to the graph and send data via server."""
        self._x.append(x)
        self._y.append(y)
        self._send_data()

    def plot(self, x, y):
        """Replace graph data entirely and send it."""
        self._x = x
        self._y = y
        self._send_data()


@deprecated_component(version="0.1.0", reason="Use LineGraph instead")
class Graph(LineGraph):
    """Line Graph component class."""

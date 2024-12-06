"""Graph class module."""

from .core import DataSenderBaseComponent


__all__ = ["Heatmap"]


class Heatmap(DataSenderBaseComponent):
    """Heatmap component class."""

    def __init__(self, component_id):
        super().__init__(component_id)
        self._x = []
        self._y = []
        self._z = []

    @property
    def data(self):
        return {
            "x": list(self._x),
            "y": list(self._y),
            "z": list(self._z),
        }

    @property
    def x(self):
        """x values, stored in a 1-D array"""
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        """y values, stored in a 1-D array"""
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y

    def append_row(self, row):
        """Add a row to the heatmap and send it to the app."""
        self._z.append(row)
        self._send_data()

    # TODO: make it like matplotlib
    def plot(self, z, x=None, y=None):
        """Replace heatmap data entirely and send it."""
        self._z = z
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        self._send_data()

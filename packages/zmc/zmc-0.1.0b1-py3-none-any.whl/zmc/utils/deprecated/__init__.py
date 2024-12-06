"""Deprecated submodule for zmc library."""

from .deprecated import *

# Remove files which are added to the namespace because of imports but are not
# meant to be accessed directly by the user.
# pylint:disable=undefined-variable
# mypy: ignore-errors
del deprecated

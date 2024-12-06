"""Utils package for zmc library."""

from .singleton import singleton
from .instance_registry import InstanceRegistry
from .logger import *
from . import deprecated

# Remove files which are added to the namespace because of imports but are not
# meant to be accessed directly by the user.
# pylint:disable=undefined-variable
# mypy: ignore-errors
del instance_registry, logger

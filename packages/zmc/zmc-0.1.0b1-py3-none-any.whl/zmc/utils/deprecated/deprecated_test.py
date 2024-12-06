import pytest

from .deprecated import custom_deprecated  # Replace with the actual import


DEPRECATION_MESSAGE = "This function is deprecated."


@custom_deprecated(version="0.1", reason=DEPRECATION_MESSAGE)
def deprecated_function():
    return "Deprecated!"


def test_deprecation_warning():
    with pytest.warns(DeprecationWarning, match=DEPRECATION_MESSAGE):
        assert deprecated_function() == "Deprecated!"

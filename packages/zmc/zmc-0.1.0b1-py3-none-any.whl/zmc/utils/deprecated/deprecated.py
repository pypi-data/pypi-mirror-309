"""Custom deprecated decorator module."""

import logging
import warnings

from functools import wraps
import deprecated.classic

__all__ = ["deprecated_component"]


def custom_deprecated(
    *args, extra_stacklevel=0, custom_showwarning=None, **kwargs
):
    """Custom decorator that extends `@deprecated` with kwargs.

    Extra kwargs:
        - custom_showwarning (fn): custom showwarning function to use
    """

    def decorator(cls_or_func):
        # Apply original @deprecated decorator
        # Increase the stacklevel, add 1 to account for this wrapper.
        decorated_func = deprecated.deprecated(
            *args, extra_stacklevel=extra_stacklevel + 1, **kwargs)(cls_or_func)

        @wraps(cls_or_func)
        def wrapped(*w_args, **w_kwargs):
            original_showwarning = warnings.showwarning
            try:
                if custom_showwarning:
                    warnings.showwarning = custom_showwarning
                return decorated_func(*w_args, **w_kwargs)
            finally:
                # Restore the original values
                warnings.showwarning = original_showwarning

        return wrapped

    return decorator


def send_warnings_to_logs(msg, category, fname, lineno, _f=None, line=None):
    """Custom showwarning function for component warnings."""
    logging.warning(warnings.formatwarning(msg, category, fname, lineno, line))


def deprecated_component(*args, **kwargs):
    """Custom @deprecated decorator with custom defaults and values."""
    if "action" not in kwargs:
        kwargs["action"] = "default"

    return custom_deprecated(
        *args,
        extra_stacklevel=1,
        custom_showwarning=send_warnings_to_logs,
        **kwargs,
    )

"""Exceptions module."""


class SincproValidationError(Exception):
    """Validation error exception."""

    def __init__(self, message):
        self.message = message

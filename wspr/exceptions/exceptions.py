# -*- coding: utf-8 -*-


class WhisperException(Exception):
    """Generic whisper library exception."""

    def __init__(self):
        """No specific message given."""
        self.value = ""

# -*- coding: utf-8 -*-


class WhisperException(Exception):
    """Generic whisper library exception."""

    def __init__(self):
        """No specific message given."""
        self.value = ""


class CodecNotSupportedError(WhisperException):
    """Thrown when receiving an audio packet from an unsupported codec."""

    def __init__(self, value):
        """"""
        self.value = value

    def __str__(self):
        """"""
        return repr(self.value)


class InvalidFormatError(WhisperException):
    """Thrown when receiving a packet we can't decode."""

    def __init__(self, value):
        """"""
        self.value = value

    def __str__(self):
        """"""
        return repr(self.value)


class InvalidVarInt(WhisperException):
    """Thrown when trying to decode an invalid variable integer."""

    def __init__(self, value):
        """"""
        self.value = value

    def __str__(self):
        """"""
        return repr(self.value)

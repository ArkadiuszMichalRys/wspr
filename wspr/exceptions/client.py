# -*- coding: utf-8 -*-
from wspr.exceptions.exceptions import WhisperException


class UnknownEventError(WhisperException):
    """Thrown when accessing an unknown event."""

    def __init__(self, value):
        """"""
        self.value = value

    def __str__(self):
        """"""
        return 'Event "{}" does not exists.'.format(self.value)


class UnknownChannelError(WhisperException):
    """Thrown accessing an unknown channel."""

    def __init__(self, value):
        """"""
        self.value = value

    def __str__(self):
        """"""
        return "Channel '{}' could not be found.".format(self.value)


class InvalidSoundDataError(WhisperException):
    """Thrown when trying to send an invalid audio pcm data packet."""

    def __init__(self, value):
        """"""
        self.value = value

    def __str__(self):
        """"""
        return repr(self.value)

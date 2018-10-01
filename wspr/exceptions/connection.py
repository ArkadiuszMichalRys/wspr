# -*- coding: utf-8 -*-

from wspr.exceptions.exceptions import WhisperException


class AlreadyConnectedError(WhisperException):
    """Thrown when we try to connect while already connected."""

    def __init__(self):
        self.value = ""

    def __str__(self):
        return "Already connected.".format(self.value)


class ConnectionRejectedError(WhisperException):
    """Thrown when server rejects our _connection."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

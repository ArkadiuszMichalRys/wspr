# -*- coding: utf-8 -*-


class Response:
    """A response from whisper notifying the user some event occurred."""

    def __init__(self, packet):
        """Contains packet which triggered response."""
        self.packet = packet

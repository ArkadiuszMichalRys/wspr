# -*- coding: utf-8 -*-


import logging


class Ping:
    """"""

    def __init__(self):
        """Mumble requires keeping track of latency/ping statistics in order to stay connected."""
        self._logger = logging.getLogger('whisper')
        # Time the last ping packet was received in unix time (milliseconds)
        self.time_received = 0
        # Time the last ping packet was sent in unix time (milliseconds)
        self.time_sent = 0
        # The number of measurements used for the average
        self.amount_of_data_points = 0
        # Average ping in milliseconds
        self.average = 40.0
        # Ping variance in milliseconds
        self.variance = 0
        # Time in between pings before we need to send another one (milliseconds)
        self.delay_milliseconds = min(10 * 1000, 30 * 1000)
        # Time in between pings before we can assume the connection has been lost (milliseconds)
        self.timeout_milliseconds = 60 * 1000

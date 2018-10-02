# -*- coding: utf-8 -*-


import logging
import time


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

    @staticmethod
    def __get_current_time_milliseconds() -> int:
        """"""
        return int(time.time() * 1000)

    def update(self) -> None:
        """"""
        self.time_sent = self.__get_current_time_milliseconds()

    def __get_travel_time(self) -> int:
        """
        Two-way travel time in milliseconds. (RTT)
        Time between the packet we send and the response.
        """
        return self.time_received - self.time_sent

    def received(self) -> None:
        """"""
        self.time_received = self.__get_current_time_milliseconds()
        travel_time = self.__get_travel_time()

        # We'll need the old average to calculate the variance
        previous_average = self.average
        # Calculate average using previous average with one more data point
        self.average = ((self.average * self.amount_of_data_points) + travel_time) / (self.amount_of_data_points + 1)

        # Variance
        try:
            # The average of the squared differences from the mean
            a = pow(previous_average - self.average, 2)
            b = self.amount_of_data_points
            c = pow(travel_time - self.average, 2)
            self.variance += a + c / b
        except ZeroDivisionError:
            self._logger.debug("Divide by zero on ping statistics.")

        # We now have one extra data point
        self.amount_of_data_points += 1

    def is_needed(self) -> bool:
        """"""
        return self.__get_current_time_milliseconds() >= self.time_sent + self.delay_milliseconds

    def has_timed_out(self) -> bool:
        """Did we get a response to our ping in the last 60 seconds?"""
        return self.time_received != 0 and self.time_sent > self.time_received + self.timeout_milliseconds

    def __repr__(self) -> str:
        """"""
        return "Ping"

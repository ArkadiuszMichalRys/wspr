# -*- coding: utf-8 -*-

import logging
import socket
import ssl
import enum

from wspr.containers.address import Address
from wspr.containers.credentials import Credentials


class ConnectionState(enum.Enum):
    """"""
    NOT_CONNECTED = 0
    AUTHENTICATING = 1
    CONNECTED = 2
    FAILED = 3


class Connection:
    """"""

    def __init__(self, address: Address, credentials: Credentials, logger: logging.Logger):
        """"""
        # Basic logging
        self._logger = logger

        # Login information
        self.address = address
        self.credentials = credentials
        self.tokens = []

        # State of the connection
        self.state = ConnectionState.NOT_CONNECTED
        self.control_socket = None
        self.media_socket = None
        self.udp_active = False
        self.receive_buffer = bytes()
        # How many bytes to read at a time from the control address, in bytes
        self.read_buffer_size = 4096
        # Total outgoing bitrate in bit/seconds
        self.bandwidth = 192000
        self.bandwidth_limit = None
        self.rate = 0.01

    def prepare_socket(self) -> None:
        """"""
        # Create SSL tunnel
        self._logger.debug("Creating SSL tunnel")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        self.control_socket = ssl.wrap_socket(
            sock,
            certfile=self.credentials.certificate_file,
            keyfile=self.credentials.key_file,
            ssl_version=ssl.PROTOCOL_TLS,
        )

    def connect(self) -> None:
        """Connect to the server."""
        self._logger.debug("Connecting")

        # Connect using the SSL tunnel
        self.control_socket.connect((self.address.host, self.address.port))
        self.control_socket.setblocking(False)

    def disconnect(self) -> None:
        """"""
        self._logger.debug("Disconnecting")
        try:
            self.control_socket.close()
        except socket.error:
            self._logger.debug("Failed to close socket. Maybe it's already closed")
        self.state = ConnectionState.NOT_CONNECTED

    def read_buffer(self) -> None:
        """Grab messages from the buffer."""
        try:
            self.receive_buffer += self.control_socket.recv(self.read_buffer_size)
        except socket.error:
            self._logger.error("Could not read socket data")

    def is_connected(self) -> bool:
        """"""
        return self.state == ConnectionState.CONNECTED

    def is_authenticating(self) -> bool:
        """"""
        return self.state == ConnectionState.AUTHENTICATING

    def __enter__(self) -> 'Connection':
        """"""
        self.prepare_socket()
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """"""
        self.disconnect()

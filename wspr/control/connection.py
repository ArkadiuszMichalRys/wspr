# -*- coding: utf-8 -*-

import logging
import select
import socket
import ssl
import struct
import enum
from typing import List, Optional

from wspr import __version__
from wspr.containers.address import Address
from wspr.containers.credentials import Credentials
from wspr.containers.ping import Ping
from wspr.exceptions.connection import AlreadyConnectedError
from wspr.protocol.packet_type import PacketType
from wspr.protocol.packets import Packet, VersionPacket, AuthenticatePacket, PingPacket


class ConnectionState(enum.Enum):
    """"""
    NOT_CONNECTED = 0
    AUTHENTICATING = 1
    CONNECTED = 2
    FAILED = 3


class Connection:
    """All traffic from client to server and vice-versa passes through here."""

    def __init__(self, address: Address, credentials: Credentials, logger: logging.Logger):
        """"""
        # Basic logging
        self._logger: logging.Logger = logger

        # Login information
        self.address: Address = address
        self.credentials: Credentials = credentials
        self.tokens: List = []

        # State of the connection
        self.state: ConnectionState = ConnectionState.NOT_CONNECTED
        self.control_socket: Optional[socket.socket] = None
        self.media_socket: Optional[socket.socket] = None
        self.ping: Ping = Ping()
        self.udp_active: bool = False
        self.receive_buffer: bytes = bytes()
        # How many bytes to read at a time from the control address, in bytes
        self.read_buffer_size: int = 4096
        # Total outgoing bitrate in bit/seconds
        self.bandwidth: int = 192000
        self.bandwidth_limit: Optional[int] = None
        self.rate: float = 0.05

    def __get_tcp_socket(self) -> socket.socket:
        """"""
        # Create SSL tunnel
        self._logger.debug("Creating SSL tunnel for TCP traffic")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock = ssl.wrap_socket(
            sock,
            certfile=self.credentials.certificate_file,
            keyfile=self.credentials.key_file,
            ssl_version=ssl.PROTOCOL_TLS,
        )
        return sock

    def __get_udp_socket(self) -> socket.socket:
        """"""
        # Create SSL tunnel
        self._logger.debug("Creating SSL tunnel for UDP traffic")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)
        sock = ssl.wrap_socket(
            sock,
            certfile=self.credentials.certificate_file,
            keyfile=self.credentials.key_file,
            ssl_version=ssl.PROTOCOL_TLS,
        )
        return sock

    def __authenticate(self) -> None:
        """"""
        self._logger.debug("Authenticating")
        # Version information
        whisper_version = __version__
        protocol_version = (1, 2, 4)
        application = "Whisper {}".format(whisper_version)
        os_string = "TODO"
        os_version_string = "TODO"

        # Send version information
        pack = VersionPacket.from_info(application, protocol_version, os_string, os_version_string).get_full()
        self.send(*pack)
        # Send user information
        pack = AuthenticatePacket.from_info(self.credentials, self.tokens).get_full()
        self.send(*pack)

        # We still need to receive a message whether we are actually authenticated
        self.state = ConnectionState.AUTHENTICATING

    def open(self) -> None:
        """Connect to the server."""
        self._logger.debug("Connecting")

        # We can't connect again if we're already connected
        if self.is_connected():
            raise AlreadyConnectedError()

        # Connect using the TCP SSL tunnel
        self.control_socket.connect((self.address.host, self.address.port))
        self.control_socket.setblocking(False)
        # Perform Mumble authentication
        self.__authenticate()
        # Connect using the UDP SSL tunnel
        if self.udp_active:
            self.media_socket.connect((self.address.host, self.address.port))
            self.media_socket.setblocking(False)

    def close(self) -> None:
        """"""
        self._logger.debug("Disconnecting")
        # TCP
        try:
            self.control_socket.close()
        except socket.error:
            self._logger.debug("Failed to close TCP socket")
        # UDP
        try:
            if self.media_socket:
                self.media_socket.close()
        except socket.error:
            self._logger.debug("Failed to close UDP socket")
        self.state = ConnectionState.NOT_CONNECTED

    def send(self, message_type: PacketType, content) -> None:
        """Send control message to the server."""
        self._logger.debug("Sending message {}':'{}".format(message_type, str(content).replace('\n', ' ')))
        # Construct content packet
        pack = struct.pack("!HL", message_type.value, content.ByteSize()) + content.SerializeToString()

        # Try sending the constructed packet
        while len(pack) > 0:
            sent = self.control_socket.send(pack)
            if sent < 0:
                self._logger.error("Server connection error")
                raise socket.error("Server connection error")
            pack = pack[sent:]

    def incoming_packets(self) -> [Packet]:
        """"""
        # Wait for incoming messages
        rlist, _, _ = select.select([self.control_socket], [], [self.control_socket], self.rate)
        # We are ready for reading
        if self.control_socket in rlist:
            self.read_buffer()
            self.receive_buffer, packets = self.converter.buffer_to_packets(self.receive_buffer)
            return packets
        return []

    def read_buffer(self) -> None:
        """Grab messages from the buffer."""
        try:
            self.receive_buffer += self.control_socket.recv(self.read_buffer_size)
        except socket.error:
            self._logger.error("Could not read socket data")

    def send_ping(self) -> None:
        """Send keep-alive packet."""
        # Send a ping packet from time to time
        if not self.ping.is_needed():
            return
        self._logger.debug("Sending ping packet")
        # Send message with current ping data
        pack = PingPacket.from_info(self.ping.average, self.ping.variance, self.ping.amount_of_data_points).get_full()
        self.send(*pack)
        # Store data for analysis
        self.ping.update()
        # We might have lost connection to the server if we didn't receive a ping for a minute
        if self.ping.has_timed_out():
            self._logger.warning("Disconnecting because of ping timeout")
            self.close()

    def incoming_ping(self) -> None:
        """Handle incoming ping packets."""
        self._logger.debug("Responding to ping")
        # Remember when the last ping packet came in
        self.ping.received()

    # def is_alive(self):
    #     """"""
    #     return self.state in (ConnectionState.CONNECTED, ConnectionState.AUTHENTICATING)

    def is_connected(self) -> bool:
        """"""
        return self.state == ConnectionState.CONNECTED

    def set_connected(self) -> None:
        self.state = ConnectionState.CONNECTED

    def is_authenticating(self) -> bool:
        """"""
        return self.state == ConnectionState.AUTHENTICATING

    def __enter__(self) -> 'Connection':
        self.control_socket = self.__get_tcp_socket()
        if self.udp_active:
            self.media_socket = self.__get_udp_socket()
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

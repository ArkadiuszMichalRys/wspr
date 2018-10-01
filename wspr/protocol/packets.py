# -*- coding: utf-8 -*-

from typing import List, Tuple

from wspr.containers.credentials import Credentials
from wspr.protocol.mumble_pb2 import (
    Version,
    Authenticate,
)
from wspr.protocol.packet_type import PacketType


class Packet:
    def __init__(self, packet):
        self.packet = packet

    def handle(self, c, r):
        raise NotImplemented


class VersionPacket(Packet):
    def __init__(self, packet):
        super().__init__(packet)

    @classmethod
    def from_info(cls, application, protocol_version, os_string, os_version_string):
        packet = Version()
        packet.release = application
        packet.version = (protocol_version[0] << 16) + (protocol_version[1] << 8) + protocol_version[2]
        packet.os = os_string
        packet.os_version = os_version_string
        return cls(packet)

    def get_full(self) -> Tuple[PacketType, Version]:
        return PacketType.VERSION, self.packet


class AuthenticatePacket(Packet):
    def __init__(self, packet):
        super().__init__(packet)

    @classmethod
    def from_info(cls, credentials: Credentials, tokens: List):
        packet = Authenticate()
        packet.username = credentials.name
        packet.password = credentials.password
        packet.tokens.extend(tokens)
        packet.opus = True
        return cls(packet)

    def get_full(self) -> Tuple[PacketType, Authenticate]:
        return PacketType.AUTHENTICATE, self.packet

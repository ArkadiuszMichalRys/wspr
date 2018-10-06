# -*- coding: utf-8 -*-

import time
from typing import List, Tuple

from wspr.containers.credentials import Credentials
from wspr.exceptions.connection import ConnectionRejectedError
from wspr.protocol.mumble_pb2 import (
    UserState,
    Version,
    Authenticate,
    Ping,
    ChannelState,
)
from wspr.protocol.packet_type import PacketType
from wspr.control.events import (
    VersionReceivedEvent,
    UDPTunnelReceivedEvent,
    AuthenticateReceivedEvent,
    PingReceivedEvent,
    RejectReceivedEvent,
    ServerSyncReceivedEvent,
    ChannelRemoveReceivedEvent,
    ChannelStateReceivedEvent,
    UserRemoveReceivedEvent,
    UserStateReceivedEvent,
    BanListReceivedEvent,
    TextMessageReceivedEvent,
    PermissionDeniedReceivedEvent,
    ACLReceivedEvent,
    QueryUsersReceivedEvent,
    CryptSetupReceivedEvent,
    ContextActionModifyReceivedEvent,
    ContextActionReceivedEvent,
    UserListReceivedEvent,
    VoiceTargetReceivedEvent,
    PermissionQueryReceivedEvent,
    CodecVersionReceivedEvent,
    UserStatsReceivedEvent,
    RequestBlobReceivedEvent,
    ServerConfigReceivedEvent,
    SuggestConfigReceivedEvent,
)


class Packet:
    """"""

    def __init__(self, packet):
        """"""
        self.packet = packet

    def handle(self, c, r):
        """"""
        raise NotImplemented


class VersionPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    @classmethod
    def from_info(cls, application, protocol_version, os_string, os_version_string):
        """"""
        packet = Version()
        packet.release = application
        packet.version = (protocol_version[0] << 16) + (protocol_version[1] << 8) + protocol_version[2]
        packet.os = os_string
        packet.os_version = os_version_string
        return cls(packet)

    def handle(self, c, r):
        """"""
        r.put(VersionReceivedEvent(self.packet))

    def get_full(self) -> Tuple[PacketType, Version]:
        """"""
        return PacketType.VERSION, self.packet


class UDPTunnelPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(UDPTunnelReceivedEvent(self.packet))
        # sound_received(self.packet)


class AuthenticatePacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    @classmethod
    def from_info(cls, credentials: Credentials, tokens: List):
        """"""
        packet = Authenticate()
        packet.username = credentials.name
        packet.password = credentials.password
        packet.tokens.extend(tokens)
        packet.opus = True
        return cls(packet)

    def handle(self, c, r):
        """"""
        r.put(AuthenticateReceivedEvent(self.packet))

    def get_full(self) -> Tuple[PacketType, Authenticate]:
        """"""
        return PacketType.AUTHENTICATE, self.packet


class PingPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(PingReceivedEvent(self.packet))
        c.incoming_ping()

    @classmethod
    def from_info(cls, average, variance, nb):
        """"""
        packet = Ping()
        packet.timestamp = int(time.time())
        packet.tcp_ping_avg = average
        packet.tcp_ping_var = variance
        packet.tcp_packets = nb
        return cls(packet)

    def get_full(self) -> Tuple[PacketType, Ping]:
        """"""
        return PacketType.PING, self.packet


class RejectPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(RejectReceivedEvent(self.packet))
        raise ConnectionRejectedError(self.packet.reason)


class ServerSyncPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(ServerSyncReceivedEvent(self.packet))
        # self._connection.current_users.set_my(mess.session)
        # c.set_bandwidth_limit(self.packet.max_bandwidth)
        if c.is_authenticating():
            c.set_connected()


class ChannelRemovePacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(ChannelRemoveReceivedEvent(self.packet))
        # self._mumble.channels.remove(message.channel_id)


class ChannelStatePacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(ChannelStateReceivedEvent(self.packet))

    def update(self, c, r, whisper):
        """"""
        self.handle(c, r)
        cs = ChannelState()
        cs.ParseFromString(self.packet)
        whisper._channels[cs.channel_id].update(cs)


class UserRemovePacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(UserRemoveReceivedEvent(self.packet))
        # information = mumble_pb2.UserRemove()
        # information.ParseFromString(args)
        # self._mumble.users.remove(information)


class UserStatePacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(UserStateReceivedEvent(self.packet))

    def update(self, c, r, whisper):
        """"""
        self.handle(c, r)
        us = UserState()
        us.ParseFromString(self.packet)
        whisper._users[us.session].update(us)


class BanListPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(BanListReceivedEvent(self.packet))


class TextMessagePacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(TextMessageReceivedEvent(self.packet))


class PermissionDeniedPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(PermissionDeniedReceivedEvent(self.packet))


class ACLPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(ACLReceivedEvent(self.packet))


class QueryUsersPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(QueryUsersReceivedEvent(self.packet))


class CryptSetupPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(CryptSetupReceivedEvent(self.packet))
        c.send_ping()


class ContextActionModifyPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(ContextActionModifyReceivedEvent(self.packet))


class ContextActionPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(ContextActionReceivedEvent(self.packet))


class UserListPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(UserListReceivedEvent(self.packet))


class VoiceTargetPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(VoiceTargetReceivedEvent(self.packet))


class PermissionQueryPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(PermissionQueryReceivedEvent(self.packet))


class CodecVersionPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(CodecVersionReceivedEvent(self.packet))
        # self._connection.sound_output.set_default_codec(mess)


class UserStatsPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(UserStatsReceivedEvent(self.packet))


class RequestBlobPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(RequestBlobReceivedEvent(self.packet))


class ServerConfigPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(ServerConfigReceivedEvent(self.packet))


class SuggestConfigPacket(Packet):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def handle(self, c, r):
        """"""
        r.put(SuggestConfigReceivedEvent(self.packet))

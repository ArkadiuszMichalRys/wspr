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

    def __init__(self, payload):
        """"""
        self.payload = payload

    def handle(self, c, r):
        """"""
        raise NotImplemented


class VersionPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    @classmethod
    def from_info(cls, application, protocol_version, os_string, os_version_string):
        """"""
        payload = Version()
        payload.release = application
        payload.version = (protocol_version[0] << 16) + (protocol_version[1] << 8) + protocol_version[2]
        payload.os = os_string
        payload.os_version = os_version_string
        return cls(payload)

    def handle(self, c, r):
        """"""
        r.put(VersionReceivedEvent(self.payload))

    def get_full(self) -> Tuple[PacketType, Version]:
        """"""
        return PacketType.VERSION, self.payload


class UDPTunnelPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(UDPTunnelReceivedEvent(self.payload))
        # sound_received(self.payload)


class AuthenticatePacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    @classmethod
    def from_info(cls, credentials: Credentials, tokens: List):
        """"""
        payload = Authenticate()
        payload.username = credentials.name
        payload.password = credentials.password
        payload.tokens.extend(tokens)
        payload.opus = True
        return cls(payload)

    def handle(self, c, r):
        """"""
        r.put(AuthenticateReceivedEvent(self.payload))

    def get_full(self) -> Tuple[PacketType, Authenticate]:
        """"""
        return PacketType.AUTHENTICATE, self.payload


class PingPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(PingReceivedEvent(self.payload))
        c.__incoming_ping()

    @classmethod
    def from_info(cls, average, variance, nb):
        """"""
        payload = Ping()
        payload.timestamp = int(time.time())
        payload.tcp_ping_avg = average
        payload.tcp_ping_var = variance
        payload.tcp_packets = nb
        return cls(payload)

    def get_full(self) -> Tuple[PacketType, Ping]:
        """"""
        return PacketType.PING, self.payload


class RejectPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(RejectReceivedEvent(self.payload))
        raise ConnectionRejectedError(self.payload.reason)


class ServerSyncPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(ServerSyncReceivedEvent(self.payload))
        # self._connection.current_users.set_my(mess.session)
        # c.set_bandwidth_limit(self.payload.max_bandwidth)
        if c.is_authenticating():
            c.set_connected()


class ChannelRemovePacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(ChannelRemoveReceivedEvent(self.payload))
        # self._mumble.channels.remove(message.channel_id)


class ChannelStatePacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(ChannelStateReceivedEvent(self.payload))

    def update(self, c, r, whisper):
        """"""
        self.handle(c, r)
        cs = ChannelState()
        cs.ParseFromString(self.payload)
        whisper._channels[cs.channel_id].update(cs)


class UserRemovePacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(UserRemoveReceivedEvent(self.payload))
        # information = mumble_pb2.UserRemove()
        # information.ParseFromString(args)
        # self._mumble.users.remove(information)


class UserStatePacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(UserStateReceivedEvent(self.payload))

    def update(self, c, r, whisper):
        """"""
        self.handle(c, r)
        us = UserState()
        us.ParseFromString(self.payload)
        whisper._users[us.session].update(us)


class BanListPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(BanListReceivedEvent(self.payload))


class TextMessagePacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(TextMessageReceivedEvent(self.payload))


class PermissionDeniedPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(PermissionDeniedReceivedEvent(self.payload))


class ACLPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(ACLReceivedEvent(self.payload))


class QueryUsersPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(QueryUsersReceivedEvent(self.payload))


class CryptSetupPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(CryptSetupReceivedEvent(self.payload))
        c.__send_ping()


class ContextActionModifyPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(ContextActionModifyReceivedEvent(self.payload))


class ContextActionPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(ContextActionReceivedEvent(self.payload))


class UserListPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(UserListReceivedEvent(self.payload))


class VoiceTargetPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(VoiceTargetReceivedEvent(self.payload))


class PermissionQueryPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(PermissionQueryReceivedEvent(self.payload))


class CodecVersionPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(CodecVersionReceivedEvent(self.payload))
        # self._connection.sound_output.set_default_codec(mess)


class UserStatsPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(UserStatsReceivedEvent(self.payload))


class RequestBlobPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(RequestBlobReceivedEvent(self.payload))


class ServerConfigPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(ServerConfigReceivedEvent(self.payload))


class SuggestConfigPacket(Packet):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def handle(self, c, r):
        """"""
        r.put(SuggestConfigReceivedEvent(self.payload))

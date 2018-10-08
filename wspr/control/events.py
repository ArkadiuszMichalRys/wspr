# -*- coding: utf-8 -*-

from wspr.protocol.mumble_pb2 import Version, Authenticate, TextMessage


class Event:
    """A response from whisper notifying the user some event occurred."""

    def __init__(self, packet):
        """Contains packet which triggered response."""
        self.packet = packet


class VersionReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        # for field, value in packet.ListFields():
        #     setattr(self, field.name, value)
        super().__init__(packet)

    def get_packet(self) -> Version:
        """"""
        # version
        # release
        # os
        # os_version
        version = Version()
        version.ParseFromString(self.packet)
        return version

    def __repr__(self) -> str:
        """"""
        v = self.get_packet()
        return "{} - {} - {} - {}".format(v.version, v.release, v.os, v.os_version)


class UDPTunnelReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def get_packet(self):
        """"""
        pass
        # self.packet = mumble_pb2.UDPTunnel().ParseFromString(packet)


class AuthenticateReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def get_packet(self):
        """"""
        auth = Authenticate()
        auth.ParseFromString(self.packet)


class PingReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class RejectReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class ServerSyncReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class ChannelRemoveReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class ChannelStateReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class UserRemoveReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class UserStateReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class BanListReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class TextMessageReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)

    def get_packet(self):
        """"""
        # actor
        # session
        # channel_id
        # tree_id
        # message
        message = TextMessage()
        message.ParseFromString(self.packet)
        return message

    def __repr__(self):
        """"""
        m = self.get_packet()
        return f"{m.message}"


class PermissionDeniedReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class ACLReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class QueryUsersReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class CryptSetupReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class ContextActionModifyReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class ContextActionReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class UserListReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class VoiceTargetReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class PermissionQueryReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class CodecVersionReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class UserStatsReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class RequestBlobReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class ServerConfigReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class SuggestConfigReceivedEvent(Event):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class FullTreeEvent(Event):
    """"""

    def __init__(self, channels, users):
        """"""
        self.channels = channels
        self.users = users
        super().__init__(None)

    def __repr__(self):
        """"""
        return "{} - {}".format(self.channels, self.users)

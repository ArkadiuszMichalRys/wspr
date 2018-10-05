# -*- coding: utf-8 -*-

from wspr.protocol.mumble_pb2 import Version, Authenticate, TextMessage


class Response:
    """A response from whisper notifying the user some event occurred."""

    def __init__(self, packet):
        """Contains packet which triggered response."""
        self.packet = packet


class VersionReceivedResponse(Response):
    def __init__(self, packet):
        # for field, value in packet.ListFields():
        #     setattr(self, field.name, value)
        super().__init__(packet)

    def get_version(self):
        # version
        # release
        # os
        # os_version
        version = Version()
        version.ParseFromString(self.packet)
        return version

    def __repr__(self):
        v = self.get_version()
        return "{} - {} - {} - {}".format(v.version, v.release, v.os, v.os_version)


class UDPTunnelReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)

    def get_tunnel(self):
        pass
        # self.packet = mumble_pb2.UDPTunnel().ParseFromString(packet)


class AuthenticateReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)

    def get_authenticate(self):
        auth = Authenticate()
        auth.ParseFromString(self.packet)


class PingReceivedResponse(Response):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class RejectReceivedResponse(Response):
    """"""

    def __init__(self, packet):
        """"""
        super().__init__(packet)


class ServerSyncReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class ChannelRemoveReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class ChannelStateReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class UserRemoveReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class UserStateReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class BanListReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class TextMessageReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)

    def get_message(self):
        # actor
        # session
        # channel_id
        # tree_id
        # message
        message = TextMessage()
        message.ParseFromString(self.packet)
        return message

    def __repr__(self):
        m = self.get_message()
        return f"{m.message}"


class PermissionDeniedReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class ACLReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class QueryUsersReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class CryptSetupReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class ContextActionModifyReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class ContextActionReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class UserListReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class VoiceTargetReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class PermissionQueryReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class CodecVersionReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class UserStatsReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class RequestBlobReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class ServerConfigReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class SuggestConfigReceivedResponse(Response):
    def __init__(self, packet):
        super().__init__(packet)


class FullTreeResponse(Response):
    def __init__(self, channels, users):
        self.channels = channels
        self.users = users
        super().__init__(None)

    def __repr__(self):
        return "{} - {}".format(self.channels, self.users)

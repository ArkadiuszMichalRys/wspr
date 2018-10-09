# -*- coding: utf-8 -*-

from wspr.protocol.mumble_pb2 import Version, Authenticate, TextMessage


class Event:
    """A response from whisper notifying the user some event occurred."""

    def __init__(self, payload):
        """Contains payload which triggered response."""
        self.payload = payload


class VersionReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        # for field, value in payload.ListFields():
        #     setattr(self, field.name, value)
        super().__init__(payload)

    def get_payload(self) -> Version:
        """"""
        # version
        # release
        # os
        # os_version
        version = Version()
        version.ParseFromString(self.payload)
        return version

    def __repr__(self) -> str:
        """"""
        v = self.get_payload()
        return "{} - {} - {} - {}".format(v.version, v.release, v.os, v.os_version)


class UDPTunnelReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def get_payload(self):
        """"""
        pass
        # self.payload = mumble_pb2.UDPTunnel().ParseFromString(payload)


class AuthenticateReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def get_payload(self):
        """"""
        auth = Authenticate()
        auth.ParseFromString(self.payload)


class PingReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class RejectReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class ServerSyncReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class ChannelRemoveReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class ChannelStateReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class UserRemoveReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class UserStateReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class BanListReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class TextMessageReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)

    def get_payload(self):
        """"""
        # actor
        # session
        # channel_id
        # tree_id
        # message
        message = TextMessage()
        message.ParseFromString(self.payload)
        return message

    def __repr__(self):
        """"""
        m = self.get_payload()
        return f"{m.message}"


class PermissionDeniedReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class ACLReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class QueryUsersReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class CryptSetupReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class ContextActionModifyReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class ContextActionReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class UserListReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class VoiceTargetReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class PermissionQueryReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class CodecVersionReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class UserStatsReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class RequestBlobReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class ServerConfigReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


class SuggestConfigReceivedEvent(Event):
    """"""

    def __init__(self, payload):
        """"""
        super().__init__(payload)


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

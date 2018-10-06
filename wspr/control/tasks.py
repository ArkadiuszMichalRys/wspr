# -*- coding: utf-8 -*-

from wspr.protocol.mumble_pb2 import TextMessage
from wspr.protocol.packet_type import PacketType


class Task:
    """A generic task to be carried out by whisper."""

    def __init__(self):
        """"""
        pass


class StartTask(Task):
    """"""

    def __init__(self):
        """"""
        super().__init__()


class StopTask(Task):
    """"""

    def __init__(self):
        """"""
        super().__init__()


class FullTreeTask(Task):
    """"""

    def __init__(self):
        """"""
        super().__init__()


class ConnectTask(Task):
    """"""

    def __init__(self):
        """"""
        super().__init__()


class MessageTask(Task):
    """"""

    def __init__(self, message):
        """"""
        self.message = message
        super().__init__()

    def get_packet(self):
        """"""
        # TODO
        p = TextMessage()
        p.session.append(0)
        p.channel_id.append(0)
        p.message = self.message
        return PacketType.TEXTMESSAGE, p


class PrivateMessageCommand(MessageTask):
    """"""

    def __init__(self, message):
        """"""
        self.message = message
        super().__init__(message)

    def get_packet(self):
        """"""
        # TODO
        p = TextMessage()
        p.session.append(0)
        p.channel_id.append(0)
        p.message = self.message
        return PacketType.TEXTMESSAGE, p


class MoveTask(Task):
    """"""

    def __init__(self, user: [int, str], channel: [int, str]):
        """"""
        self.user = user
        self.channel = channel
        super().__init__()

    def get_packet(self):
        """"""
        # TODO
        p = TextMessage()
        p.session.append(0)
        p.channel_id.append(0)
        return PacketType.USERSTATE, p

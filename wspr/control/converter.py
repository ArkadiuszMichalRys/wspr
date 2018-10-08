# -*- coding: utf-8 -*-

import logging
import struct
from typing import Optional, Tuple, List

from wspr.protocol.packets import (
    Packet,
    SuggestConfigPacket,
    ServerConfigPacket,
    RequestBlobPacket,
    UserListPacket,
    CodecVersionPacket,
    PermissionQueryPacket,
    VoiceTargetPacket,
    ContextActionPacket,
    ContextActionModifyPacket,
    CryptSetupPacket,
    QueryUsersPacket,
    ACLPacket,
    PermissionDeniedPacket,
    TextMessagePacket,
    BanListPacket,
    UserStatePacket,
    UserRemovePacket,
    ChannelStatePacket,
    ChannelRemovePacket,
    ServerSyncPacket,
    RejectPacket,
    PingPacket,
    AuthenticatePacket,
    VersionPacket,
    UDPTunnelPacket,
)
from wspr.protocol.packet_type import PacketType


class PacketConverter:
    """"""

    def __init__(self):
        """"""
        self._logger = logging.getLogger('whisper')
        self._router = {
            PacketType.UDPTUNNEL: self.udp_tunnel,
            PacketType.VERSION: self.version,
            PacketType.AUTHENTICATE: self.authenticate,
            PacketType.PING: self.ping,
            PacketType.REJECT: self.reject,
            PacketType.SERVERSYNC: self.server_sync,
            PacketType.CHANNELREMOVE: self.channel_remove,
            PacketType.CHANNELSTATE: self.channel_state,
            PacketType.USERREMOVE: self.user_remove,
            PacketType.USERSTATE: self.user_state,
            PacketType.BANLIST: self.ban_list,
            PacketType.TEXTMESSAGE: self.text_message,
            PacketType.PERMISSIONDENIED: self.permission_denied,
            PacketType.ACL: self.acl,
            PacketType.QUERYUSERS: self.query_users,
            PacketType.CRYPTSETUP: self.crypt_setup,
            PacketType.CONTEXTACTIONMODIFY: self.context_action_modify,
            PacketType.CONTEXTACTION: self.context_action,
            PacketType.USERLIST: self.user_list,
            PacketType.VOICETARGET: self.voice_target,
            PacketType.PERMISSIONQUERY: self.permission_query,
            PacketType.CODECVERSION: self.codec_version,
            PacketType.USERSTATS: self.user_stats,
            PacketType.REQUESTBLOB: self.request_blob,
            PacketType.SERVERCONFIG: self.server_config,
            PacketType.SUGGESTCONFIG: self.suggest_config,
        }

    def convert(self, packet_type, payload) -> Optional[Packet]:
        """"""
        try:
            dispatch = self._router.get(packet_type)
            return dispatch(payload)
        except KeyError:
            text = "UNHANDLED MESSAGE TYPE: {}, args: {}"
            self._logger.warning(text.format(packet_type, payload))
        return None

    def buffer_to_packets(self, buffer) -> Tuple[bytes, List[Packet]]:
        """Extract packets from buffer."""
        # Header is present (type + length)
        packets = []
        while len(buffer) >= 6:
            header = buffer[0:6]
            # Shouldn't happen, need to read more data
            if len(header) < 6:
                break
            # Decode header
            packet_type_int, size = struct.unpack("!HL", header)
            packet_type = PacketType(packet_type_int)
            # We don't have enough data yet, we'll read more later
            if len(buffer) < size + 6:
                break
            # Get message without header
            message = buffer[6:size + 6]
            # Remove what we've processed from the buffer
            buffer = buffer[size + 6:]
            # Do something with the message
            packets.append(self.convert(packet_type, message))
        return buffer, packets

    def udp_tunnel(self, payload):
        """"""
        return UDPTunnelPacket(payload)

    def version(self, payload):
        """"""
        return VersionPacket(payload)

    def authenticate(self, payload):
        """"""
        return AuthenticatePacket(payload)

    def ping(self, payload):
        """"""
        return PingPacket(payload)

    def reject(self, payload):
        """"""
        return RejectPacket(payload)

    def server_sync(self, payload):
        """"""
        return ServerSyncPacket(payload)

    def channel_remove(self, payload):
        """"""
        return ChannelRemovePacket(payload)

    def channel_state(self, payload):
        """"""
        return ChannelStatePacket(payload)

    def user_remove(self, payload):
        """"""
        return UserRemovePacket(payload)

    def user_state(self, payload):
        """"""
        return UserStatePacket(payload)

    def ban_list(self, payload):
        """"""
        return BanListPacket(payload)

    def text_message(self, payload):
        """"""
        return TextMessagePacket(payload)

    def permission_denied(self, payload):
        """"""
        return PermissionDeniedPacket(payload)

    def acl(self, payload):
        """"""
        return ACLPacket(payload)

    def query_users(self, payload):
        """"""
        return QueryUsersPacket(payload)

    def crypt_setup(self, payload):
        """"""
        return CryptSetupPacket(payload)

    def context_action_modify(self, payload):
        """"""
        return ContextActionModifyPacket(payload)

    def context_action(self, payload):
        """"""
        return ContextActionPacket(payload)

    def user_list(self, payload):
        """"""
        return UserListPacket(payload)

    def voice_target(self, payload):
        """"""
        return VoiceTargetPacket(payload)

    def permission_query(self, payload):
        """"""
        return PermissionQueryPacket(payload)

    def codec_version(self, payload):
        """"""
        return CodecVersionPacket(payload)

    def user_stats(self, payload):
        """"""
        return UserListPacket(payload)

    def request_blob(self, payload):
        """"""
        return RequestBlobPacket(payload)

    def server_config(self, payload):
        """"""
        return ServerConfigPacket(payload)

    def suggest_config(self, payload):
        """"""
        return SuggestConfigPacket(payload)

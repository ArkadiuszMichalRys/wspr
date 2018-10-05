# -*- coding: utf-8 -*-

import logging
import struct

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

    def convert(self, packet_type, packet_content) -> [None, Packet]:
        """"""
        try:
            dispatch = self._router.get(packet_type)
            return dispatch(packet_content)
        except KeyError:
            text = "UNHANDLED MESSAGE TYPE: {}, args: {}"
            self._logger.warning(text.format(packet_type, packet_content))
        return None

    def buffer_to_packets(self, buffer):
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

    def udp_tunnel(self, packet_content):
        """"""
        return UDPTunnelPacket(packet_content)

    def version(self, packet_content):
        """"""
        return VersionPacket(packet_content)

    def authenticate(self, packet_content):
        """"""
        return AuthenticatePacket(packet_content)

    def ping(self, packet_content):
        """"""
        return PingPacket(packet_content)

    def reject(self, packet_content):
        """"""
        return RejectPacket(packet_content)

    def server_sync(self, packet_content):
        """"""
        return ServerSyncPacket(packet_content)

    def channel_remove(self, packet_content):
        """"""
        return ChannelRemovePacket(packet_content)

    def channel_state(self, packet_content):
        """"""
        return ChannelStatePacket(packet_content)

    def user_remove(self, packet_content):
        """"""
        return UserRemovePacket(packet_content)

    def user_state(self, packet_content):
        """"""
        return UserStatePacket(packet_content)

    def ban_list(self, packet_content):
        """"""
        return BanListPacket(packet_content)

    def text_message(self, packet_content):
        """"""
        return TextMessagePacket(packet_content)

    def permission_denied(self, packet_content):
        """"""
        return PermissionDeniedPacket(packet_content)

    def acl(self, packet_content):
        """"""
        return ACLPacket(packet_content)

    def query_users(self, packet_content):
        """"""
        return QueryUsersPacket(packet_content)

    def crypt_setup(self, packet_content):
        """"""
        return CryptSetupPacket(packet_content)

    def context_action_modify(self, packet_content):
        """"""
        return ContextActionModifyPacket(packet_content)

    def context_action(self, packet_content):
        """"""
        return ContextActionPacket(packet_content)

    def user_list(self, packet_content):
        """"""
        return UserListPacket(packet_content)

    def voice_target(self, packet_content):
        """"""
        return VoiceTargetPacket(packet_content)

    def permission_query(self, packet_content):
        """"""
        return PermissionQueryPacket(packet_content)

    def codec_version(self, packet_content):
        """"""
        return CodecVersionPacket(packet_content)

    def user_stats(self, packet_content):
        """"""
        return UserListPacket(packet_content)

    def request_blob(self, packet_content):
        """"""
        return RequestBlobPacket(packet_content)

    def server_config(self, packet_content):
        """"""
        return ServerConfigPacket(packet_content)

    def suggest_config(self, packet_content):
        """"""
        return SuggestConfigPacket(packet_content)

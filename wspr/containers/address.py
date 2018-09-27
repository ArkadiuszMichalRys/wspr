# -*- coding: utf-8 -*-


class Address:
    """Address consisting of hostname and port."""

    def __init__(self, host: str = "localhost", port: int = 64738):
        """"""
        self.host = host
        self.port = port

    @classmethod
    def from_string(cls, socket: str) -> 'Address':
        """"""
        host, port = socket.split(":")
        return cls(host, int(port))

    def __repr__(self) -> str:
        """"""
        return "{}:{}".format(self.host, self.port)

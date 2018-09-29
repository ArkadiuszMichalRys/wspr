# -*- coding: utf-8 -*-


import pathlib


class Credentials:
    """User login information."""

    def __init__(self, name: str = "Anonymous", password: str = "", certificate_file: pathlib.Path = None,
                 key_file: pathlib.Path = None):
        """"""
        self.name = name
        self.password = password
        self.certificate_file = certificate_file
        self.key_file = key_file

    def __repr__(self) -> str:
        """"""
        text = "Cred({})"
        return text.format(self.name)

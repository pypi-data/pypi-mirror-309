"""
Generated by Sideko (sideko.dev)
"""

"""File Generated by Sideko (sideko.dev)"""

from httpx._models import Headers


class BinaryResponse:
    content: bytes
    headers: Headers

    def __init__(self, content: bytes, headers: Headers) -> None:
        self.content = content
        self.headers = headers

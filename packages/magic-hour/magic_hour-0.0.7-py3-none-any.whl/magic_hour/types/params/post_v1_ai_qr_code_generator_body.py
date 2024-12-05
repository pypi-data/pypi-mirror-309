"""
Generated by Sideko (sideko.dev)
"""

import typing
import typing_extensions
import pydantic

from .post_v1_ai_qr_code_generator_body_style import (
    PostV1AiQrCodeGeneratorBodyStyle,
    _SerializerPostV1AiQrCodeGeneratorBodyStyle,
)


class PostV1AiQrCodeGeneratorBody(typing_extensions.TypedDict):
    """ """

    content: typing_extensions.Required[str]
    name: typing.Optional[str]
    style: typing_extensions.Required[PostV1AiQrCodeGeneratorBodyStyle]


class _SerializerPostV1AiQrCodeGeneratorBody(pydantic.BaseModel):
    """
    Serializer for PostV1AiQrCodeGeneratorBody handling case conversions
    and file omitions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    content: str = pydantic.Field(alias="content")
    name: typing.Optional[str] = pydantic.Field(alias="name")
    style: _SerializerPostV1AiQrCodeGeneratorBodyStyle = pydantic.Field(alias="style")

"""
Generated by Sideko (sideko.dev)
"""

import typing
import typing_extensions
import pydantic

from .post_v1_ai_image_generator_body_style import (
    PostV1AiImageGeneratorBodyStyle,
    _SerializerPostV1AiImageGeneratorBodyStyle,
)


class PostV1AiImageGeneratorBody(typing_extensions.TypedDict):
    """ """

    image_count: typing_extensions.Required[float]
    name: typing.Optional[str]
    orientation: typing_extensions.Required[
        typing_extensions.Literal["landscape", "portrait", "square"]
    ]
    style: typing_extensions.Required[PostV1AiImageGeneratorBodyStyle]


class _SerializerPostV1AiImageGeneratorBody(pydantic.BaseModel):
    """
    Serializer for PostV1AiImageGeneratorBody handling case conversions
    and file omitions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    image_count: float = pydantic.Field(alias="image_count")
    name: typing.Optional[str] = pydantic.Field(alias="name")
    orientation: typing_extensions.Literal["landscape", "portrait", "square"] = (
        pydantic.Field(alias="orientation")
    )
    style: _SerializerPostV1AiImageGeneratorBodyStyle = pydantic.Field(alias="style")

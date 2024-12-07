from typing import Literal, Optional

from pydantic import Field

from pydantic_api.base import BaseModel


TextAnnotationColorLiteral = Literal[
    "default",
    "blue",
    "blue_background",
    "brown",
    "brown_background",
    "default",
    "gray",
    "gray_background",
    "green",
    "green_background",
    "orange",
    "orange_background",
    "pink",
    "pink_background",
    "purple",
    "purple_background",
    "red",
    "red_background",
    "yellow",
    "yellow_background",
]


class TextAnnotations(BaseModel):
    """Text style annotations for rich text."""

    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: TextAnnotationColorLiteral


RichTextTypeLiteral = Literal["text", "mention", "equation"]


class BaseRichTextObject(BaseModel):
    """Base model for Rich Text."""

    type: RichTextTypeLiteral
    annotations: Optional[TextAnnotations] = Field(
        None, description="Formatting style for the text"
    )
    plain_text: Optional[str] = Field(None)
    href: Optional[str] = Field(None, description="Hyperlink for the text")


__all__ = [
    "TextAnnotationColorLiteral",
    "TextAnnotations",
    "RichTextTypeLiteral",
    "BaseRichTextObject",
]

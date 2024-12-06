from typing import Union, Literal

from .emoji import EmojiObject
from .file import ExternalFileObject


IconObject = Union[ExternalFileObject, EmojiObject]


class IconObjectFactory:
    @classmethod
    def from_external_file(cls, url: str):
        return ExternalFileObject.from_url(url=url)

    @classmethod
    def from_emoji(cls, emoji: str):
        """Create a new IconObject with emoji.

        Args:
            emoji: The emoji to use.
        """
        return EmojiObject(emoji=emoji)


CoverObject = ExternalFileObject


class CoverObjectFactory:
    @classmethod
    def from_external_file(cls, url: str):
        return ExternalFileObject.from_url(url=url)


ColorLiteral = Literal[
    "default",
    "gray",
    "brown",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "pink",
    "red",
]


__all__ = [
    "IconObject",
    "IconObjectFactory",
    "CoverObject",
    "CoverObjectFactory",
    "ColorLiteral",
]

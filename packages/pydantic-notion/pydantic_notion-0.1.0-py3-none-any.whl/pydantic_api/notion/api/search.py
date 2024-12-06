from typing import Union

from .base import NotionPaginatedData
from ..entities import (
    Page,
    Database,
)

SearchByTitleResponse = NotionPaginatedData[Union[Page, Database]]
"""Reference: https://developers.notion.com/reference/post-search"""


__all__ = [
    "SearchByTitleResponse",
]

from typing import Union

from .base import NotionPaginatedData
from ..entities import (
    Page,
    CheckboxProperty,
    CreatedByProperty,
    CreatedTimeProperty,
    DateProperty,
    EmailProperty,
    FilesProperty,
    LastEditedByProperty,
    LastEditedTimeProperty,
    MultiSelectProperty,
    NumberProperty,
    PhoneNumberProperty,
    SelectProperty,
    StatusProperty,
    URLProperty,
    TitleProperty,
    RichTextProperty,
    PeopleProperty,
    RelationProperty,
    RollupProperty,
    UniqueIDProperty,
    FormulaProperty,
    VerificationProperty,
)


CreatePageResponse = Page
"""Reference: https://developers.notion.com/reference/post-page"""

RetrievePageResponse = Page
"""Reference: https://developers.notion.com/reference/retrieve-a-page"""

SimplePageProperty = Union[
    CheckboxProperty,
    CreatedByProperty,
    CreatedTimeProperty,
    DateProperty,
    EmailProperty,
    FilesProperty,
    LastEditedByProperty,
    LastEditedTimeProperty,
    MultiSelectProperty,
    NumberProperty,
    PhoneNumberProperty,
    SelectProperty,
    StatusProperty,
    URLProperty,
    RollupProperty,
    UniqueIDProperty,
    FormulaProperty,
    VerificationProperty,
]
"""Reference: https://developers.notion.com/reference/retrieve-a-page-property#simple-properties"""

PaginatedPageProperty = Union[
    TitleProperty,
    RichTextProperty,
    PeopleProperty,
    RelationProperty,
]
"""Reference: https://developers.notion.com/reference/retrieve-a-page-property#paginated-properties"""

RetrievePagePropertyItemResponse = Union[
    SimplePageProperty, NotionPaginatedData[PaginatedPageProperty]
]
"""Reference: https://developers.notion.com/reference/retrieve-a-page-property"""

UpdatePagePropertiesResponse = Page
"""Reference: https://developers.notion.com/reference/patch-page"""


__all__ = [
    "CreatePageResponse",
    "RetrievePageResponse",
    "RetrievePagePropertyItemResponse",
    "UpdatePagePropertiesResponse",
]

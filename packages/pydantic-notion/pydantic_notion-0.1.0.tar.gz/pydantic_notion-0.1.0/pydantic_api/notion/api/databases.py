from typing import Union

from .base import NotionPaginatedData
from ..entities import Database, Page


CreateDatabaseResponse = Database
"""Reference: https://developers.notion.com/reference/create-a-database"""

QueryDatabaseResponse = NotionPaginatedData[Union[Database, Page]]
"""Reference: https://developers.notion.com/reference/post-database-query"""

RetrieveDatabaseResponse = Database
"""Reference: https://developers.notion.com/reference/retrieve-a-database"""

UpdateDatabaseResponse = Database
"""Reference: https://developers.notion.com/reference/update-a-database"""


__all__ = [
    "CreateDatabaseResponse",
    "QueryDatabaseResponse",
    "RetrieveDatabaseResponse",
    "UpdateDatabaseResponse",
]

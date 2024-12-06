from .base import NotionPaginatedData
from ..entities import UserObject, BotUserObject


ListAllUsersResponse = NotionPaginatedData[UserObject]
"""Reference: https://developers.notion.com/reference/get-users"""

RetrieveUserResponse = UserObject
"""Reference: https://developers.notion.com/reference/get-user"""

RetrieveBotUserResponse = BotUserObject
"""Reference: https://developers.notion.com/reference/get-self"""

__all__ = [
    "ListAllUsersResponse",
    "RetrieveUserResponse",
    "RetrieveBotUserResponse",
]

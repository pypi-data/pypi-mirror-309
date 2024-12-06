from .base import NotionPaginatedData
from ..entities import CommentObject


CreateCommentResponse = CommentObject
"""Reference: https://developers.notion.com/reference/create-a-comment"""

RetrieveCommentsResponse = NotionPaginatedData[CommentObject]
"""Reference: https://developers.notion.com/reference/retrieve-a-comment"""


__all__ = [
    "CreateCommentResponse",
    "RetrieveCommentsResponse",
]

"""
Reference: https://developers.notion.com/reference/parent-object
"""

from enum import StrEnum
from typing import Literal, Union, Annotated

from uuid import UUID
from pydantic import Field

from pydantic_api.base import BaseModel


class ParentObjectTypeEnum(StrEnum):
    DATABASE_ID = "database_id"
    PAGE_ID = "page_id"
    WORKSPACE = "workspace"
    BLOCK_ID = "block_id"


class DatabaseParentObject(BaseModel):
    """Database as a parent."""

    type: Literal[ParentObjectTypeEnum.DATABASE_ID] = ParentObjectTypeEnum.DATABASE_ID
    database_id: UUID


class PageParentObject(BaseModel):
    """Page as a parent."""

    type: Literal[ParentObjectTypeEnum.PAGE_ID] = ParentObjectTypeEnum.PAGE_ID
    page_id: UUID


class WorkspaceParentObject(BaseModel):
    """Workspace as a parent. I.e. a root-level page in the workspace."""

    type: Literal[ParentObjectTypeEnum.WORKSPACE] = ParentObjectTypeEnum.WORKSPACE
    workspace: Literal[True] = True


class BlockParentObject(BaseModel):
    """Block as a parent."""

    type: Literal[ParentObjectTypeEnum.BLOCK_ID] = ParentObjectTypeEnum.BLOCK_ID
    block_id: UUID


ParentObject = Annotated[
    Union[
        DatabaseParentObject, PageParentObject, WorkspaceParentObject, BlockParentObject
    ],
    Field(discriminator="type"),
]


# The following classes are util classes which are not mentioned in the Notion API documentation.
class ParentObjectFactory:
    @classmethod
    def from_page_id(cls, page_id: UUID) -> PageParentObject:
        return PageParentObject(page_id=page_id)

    @classmethod
    def from_database_id(cls, database_id: UUID) -> DatabaseParentObject:
        return DatabaseParentObject(database_id=database_id)

    @classmethod
    def from_workspace(cls) -> WorkspaceParentObject:
        return WorkspaceParentObject()

    @classmethod
    def from_block_id(cls, block_id: UUID) -> BlockParentObject:
        return BlockParentObject(block_id=block_id)


__all__ = [
    "ParentObjectTypeEnum",
    "DatabaseParentObject",
    "PageParentObject",
    "WorkspaceParentObject",
    "BlockParentObject",
    "ParentObject",
    "ParentObjectFactory",
]

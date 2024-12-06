"""
Reference: https://developers.notion.com/reference/property-schema-object
"""

from typing import List, Optional, Literal, Union, Annotated

from uuid import UUID
from pydantic import Field, model_validator

from pydantic_api.base import BaseModel
from ..common import ColorLiteral
from .common import (
    SelectOption,
    DatabasePropertyTypeLiteral,
    RelationTypeLiteral,
    NumberFormatLiteral,
    RollupFunctionLiteral,
)


class EmptyConfig(BaseModel):
    pass


class BaseDatabaseProperty(BaseModel):
    id: Optional[str] = Field(
        None,
        description='An identifier for the property, usually a short string of random letters and symbols. Some automatically generated property types have special human-readable IDs. For example, all Title properties have an id of "title".',
    )
    name: Optional[str] = Field(
        None, description="The name of the property as it appears in Notion."
    )
    description: Optional[str] = Field(
        None, description="The description of the property as it appears in Notion."
    )
    type: DatabasePropertyTypeLiteral


# Specific Database Property Schemas
class CheckboxDatabaseProperty(BaseDatabaseProperty):
    type: Literal["checkbox"] = "checkbox"
    checkbox: EmptyConfig


class CreatedByDatabaseProperty(BaseDatabaseProperty):
    type: Literal["created_by"] = "created_by"
    created_by: EmptyConfig


class CreatedTimeDatabaseProperty(BaseDatabaseProperty):
    type: Literal["created_time"] = "created_time"
    created_time: EmptyConfig


class DateDatabaseProperty(BaseDatabaseProperty):
    type: Literal["date"] = "date"
    date: EmptyConfig


class EmailDatabaseProperty(BaseDatabaseProperty):
    type: Literal["email"] = "email"
    email: EmptyConfig


class FilesDatabaseProperty(BaseDatabaseProperty):
    """
    Note: The Notion API does not yet support uploading files to Notion.

    A files database property is rendered in the Notion UI as a column that has values that are either files uploaded directly to Notion or external links to files. The files type object is empty; there is no additional configuration.
    """

    type: Literal["files"] = "files"
    files: EmptyConfig


# formula
class FormulaPropertyConfig(BaseModel):
    expression: str = Field(
        ...,
        description="The formula that is used to compute the values for this property. Refer to https://www.notion.so/help/formulas",
    )


class FormulaDatabaseProperty(BaseDatabaseProperty):
    type: Literal["formula"] = "formula"
    formula: FormulaPropertyConfig


# last_edited_by
class LastEditedByDatabaseProperty(BaseDatabaseProperty):
    type: Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: EmptyConfig


# last_edited_time
class LastEditedTimeDatabaseProperty(BaseDatabaseProperty):
    type: Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: EmptyConfig


# multi_select
class MultiSelectPropertyConfig(BaseModel):
    options: List[SelectOption] = Field(default_factory=list)


class MultiSelectDatabaseProperty(BaseDatabaseProperty):
    type: Literal["multi_select"] = "multi_select"
    multi_select: MultiSelectPropertyConfig


# number
class NumberPropertyConfig(BaseModel):
    format: Optional[NumberFormatLiteral] = Field(None)


class NumberDatabaseProperty(BaseDatabaseProperty):
    type: Literal["number"] = "number"
    number: NumberPropertyConfig = Field(default_factory=NumberPropertyConfig)


# people
class PeopleDatabaseProperty(BaseDatabaseProperty):
    type: Literal["people"] = "people"
    people: EmptyConfig


# phone_number
class PhoneNumberDatabaseProperty(BaseDatabaseProperty):
    type: Literal["phone_number"] = "phone_number"
    phone_number: EmptyConfig


# relation
class RelationPropertyConfig(BaseModel):
    type: Optional[RelationTypeLiteral] = None
    database_id: UUID = Field(
        ...,
        description="The database that the relation property refers to. The corresponding linked page values must belong to the database in order to be valid.",
    )
    synced_property_id: Optional[str] = Field(
        ...,
        description="The id of the corresponding property that is updated in the related database when this property is changed.",
    )
    synced_property_name: Optional[str] = Field(
        ...,
        description="The name of the corresponding property that is updated in the related database when this property is changed.",
    )

    @model_validator(mode="after")
    def ensure_either_name_or_id_is_provided(self):
        if self.type == "single_property":
            if self.synced_property_name is None and self.synced_property_id is None:
                raise ValueError(
                    "Either synced_property_name or synced_property_id is required."
                )
        elif self.type == "dual_property":
            pass
        return self


class RelationDatabaseProperty(BaseDatabaseProperty):
    type: Literal["relation"] = "relation"
    relation: RelationPropertyConfig


# rich_text
class RichTextDatabaseProperty(BaseDatabaseProperty):
    type: Literal["rich_text"] = "rich_text"
    rich_text: EmptyConfig


# rollup
class RollupPropertyConfig(BaseModel):
    relation_property_name: Optional[str] = None
    relation_property_id: Optional[str] = None
    rollup_property_name: Optional[str] = None
    rollup_property_id: Optional[str] = None
    function: RollupFunctionLiteral

    @model_validator(mode="after")
    def ensure_either_name_or_id_is_provided(self):
        if self.relation_property_name is None and self.relation_property_id is None:
            raise ValueError(
                "Either relation_property_name or relation_property_id is required."
            )
        if self.rollup_property_name is None and self.rollup_property_id is None:
            raise ValueError(
                "Either rollup_property_name or rollup_property_id is required."
            )
        return self


class RollupDatabaseProperty(BaseDatabaseProperty):
    type: Literal["rollup"] = "rollup"
    rollup: RollupPropertyConfig


# select
class SelectOption(BaseModel):
    id: Optional[str] = Field(
        None,
        description="An identifier for the option. It doesn't change if the name is changed. These are sometimes, but not always, UUIDs.",
    )
    name: Optional[str] = Field(
        None, description="The name of the option as it appears in the Notion UI."
    )
    color: Optional[ColorLiteral] = Field(None)


class SelectPropertyConfig(BaseModel):
    options: List[SelectOption] = Field(default_factory=list)


class SelectDatabaseProperty(BaseDatabaseProperty):
    type: Literal["select"] = "select"
    select: SelectPropertyConfig = Field(default_factory=SelectPropertyConfig)


# status
class StatusOption(BaseModel):
    color: Optional[ColorLiteral] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)


class StatusGroup(BaseModel):
    color: Optional[ColorLiteral] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    option_ids: Optional[List[UUID]] = Field(
        None,
        description="A sorted list of ids of all of the options that belong to a group.",
    )


class StatusPropertyConfig(BaseModel):
    options: List[StatusOption] = Field(default_factory=list)
    group: Optional[List[StatusGroup]] = Field(default_factory=list)


class StatusDatabaseProperty(BaseDatabaseProperty):
    """
    Note: It is not possible to update a status database property's name or options values via the API.
    """

    type: Literal["status"] = "status"
    status: StatusPropertyConfig


# title
class TitleDatabaseProperty(BaseDatabaseProperty):
    type: Literal["title"] = "title"
    title: EmptyConfig


# url
class URLDatabaseProperty(BaseDatabaseProperty):
    type: Literal["url"] = "url"
    url: EmptyConfig


# Union for all Database Schema Properties
DatabaseProperty = Annotated[
    Union[
        CheckboxDatabaseProperty,
        CreatedByDatabaseProperty,
        CreatedTimeDatabaseProperty,
        DateDatabaseProperty,
        EmailDatabaseProperty,
        FilesDatabaseProperty,
        FormulaDatabaseProperty,
        LastEditedByDatabaseProperty,
        LastEditedTimeDatabaseProperty,
        MultiSelectDatabaseProperty,
        NumberDatabaseProperty,
        PeopleDatabaseProperty,
        PhoneNumberDatabaseProperty,
        RelationDatabaseProperty,
        RichTextDatabaseProperty,
        RollupDatabaseProperty,
        SelectDatabaseProperty,
        StatusDatabaseProperty,
        TitleDatabaseProperty,
        URLDatabaseProperty,
    ],
    Field(discriminator="type"),
]


__all__ = [
    "CheckboxDatabaseProperty",
    "CreatedByDatabaseProperty",
    "CreatedTimeDatabaseProperty",
    "DateDatabaseProperty",
    "EmailDatabaseProperty",
    "FilesDatabaseProperty",
    "FormulaDatabaseProperty",
    "LastEditedByDatabaseProperty",
    "LastEditedTimeDatabaseProperty",
    "MultiSelectDatabaseProperty",
    "NumberDatabaseProperty",
    "PeopleDatabaseProperty",
    "PhoneNumberDatabaseProperty",
    "RelationDatabaseProperty",
    "RichTextDatabaseProperty",
    "RollupDatabaseProperty",
    "SelectDatabaseProperty",
    "StatusDatabaseProperty",
    "TitleDatabaseProperty",
    "URLDatabaseProperty",
    # Union Type
    "DatabaseProperty",
]

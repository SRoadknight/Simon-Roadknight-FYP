from datetime import datetime
from typing import TYPE_CHECKING, Union
from sqlmodel import SQLModel, Field, Relationship, Column, AutoString, text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import field_validator
from src.utils import validate_website_url
from src.skill_tags.models import SkillTagRead
from src.models import Name


if TYPE_CHECKING:
    from src.groups.models import Group
    from src.skill_tags.models import SkillTag


# This is the content posts that will be created by the staff
# and assigned to groups
    
# Content could be enhanced with something liek tags, or keywords
# this pseudo happens by it being assocaited with a group
# this could also be done by giving additional detail to skills 
    

class ContentBase(SQLModel):
    title: Name = Field(max_length=50, sa_type=AutoString)
    content: Union[dict, None] = Field(sa_column=Column(JSONB), default=None)
    website_url: Union[str, None] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True

    _validate_content_url = field_validator("website_url")(validate_website_url)

class Content(ContentBase, table=True):
    __tablename__ = "content"
    id: int = Field(primary_key=True, default=None)
    date_posted: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )
    last_updated: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()"), 
        onupdate=text("now()")),
    )
   

    groups: list["ContentGroup"] = Relationship(back_populates="content")
    skills: list["ContentSkillTag"] = Relationship(back_populates="content")

    
class ContentCreate(ContentBase):
    pass

class ContentUpdate(SQLModel):
    title: Union[Name, None] = None
    content: Union[dict, None] = None
    website_url: Union[str, None] = None
    published: Union[bool, None] = None

    _validate_content_url = field_validator("website_url")(validate_website_url)

class ContentRead(ContentBase):
    pass


# Add content to group (content can be part of multiple groups)

class ContentGroupBase(SQLModel):
    pass

class ContentGroup(ContentGroupBase, table=True):
    __tablename__ = "content_group"
    content_id: int = Field(foreign_key="content.id", primary_key=True)
    group_id: int = Field(foreign_key="group.id", primary_key=True)
    date_assigned: datetime = Field(
        default=datetime.now(),
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )

    content: "Content" = Relationship(back_populates="groups")
    group: "Group" = Relationship(back_populates="content")

class ContentGroupCreate(ContentGroupBase):
    pass

class ContentGroupRead(ContentGroupBase):
    content: "ContentRead"

class ContentGroupUpdate(SQLModel):
    pass

# content skill tags

class ContentSkillTagBase(SQLModel):
    pass

class ContentSkillTag(ContentSkillTagBase, table=True):
    __tablename__ = "content_skill_tags"
    content_id: int = Field(foreign_key="content.id", primary_key=True)
    skill_id: int = Field(foreign_key="skill_tag.id", primary_key=True)
    date_added: datetime = Field(
        default=datetime.now(),
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )

    content: "Content" = Relationship(back_populates="skills")
    skill: "SkillTag" = Relationship(back_populates="content")
    
class ContentSkillTagCreate(ContentSkillTagBase):
    content_id: int
    skill_id: int

class ContentSkillTagRead(ContentSkillTagBase):
    date_added: datetime
    skill: SkillTagRead
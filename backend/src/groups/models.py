from datetime import datetime
from typing import TYPE_CHECKING, Union
from sqlmodel import SQLModel, Field, Relationship, AutoString, Column, text, TIMESTAMP
from src.models import ConstrainedId
from src.content.models import ContentGroupRead
from src.models import ConstrainedId, Name, Description



if TYPE_CHECKING:
    from src.students.models import Student
    from src.content.models import ContentGroup


# This will be the groups that content and students will be assigned to

class GroupBase(SQLModel):
    name: Name = Field(max_length=50, sa_type=AutoString, unique=True)
    description: Description = Field(default=None, max_length=250, sa_type=AutoString)

class Group(GroupBase, table=True):
    __tablename__ = "group"
    id: int = Field(primary_key=True, default=None)
    date_created: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )

    students: list["GroupMember"] = Relationship(back_populates="group")
    content: list["ContentGroup"]= Relationship(back_populates="group")

class GroupCreate(GroupBase):
    pass

class GroupRead(GroupBase):
    pass

class GroupReadWithContent(GroupRead):
    content: list["ContentGroupRead"] = []

class GroupReadWithMembers(GroupRead):
    students: list["GroupMemberRead"] = []

class GroupUpdate(SQLModel):
    name: Union[Name, None] = None
    description: Union[Description, None] = None


# Table for the student group members model

class GroupMemberBase(SQLModel):
    pass

class GroupMember(GroupMemberBase, table=True):
    __tablename__ = "student_group_membership"
    student_id: ConstrainedId = Field(foreign_key="student.id", primary_key=True, sa_type=AutoString)
    group_id: int = Field(foreign_key="group.id", primary_key=True)
    date_joined: datetime = Field(
        default=datetime.now(),
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )


    student: "Student" = Relationship(back_populates="groups")
    group: "Group" = Relationship(back_populates="students")

class GroupMemberCreate(GroupMemberBase):
    student_id: ConstrainedId
    group_id: int

class GroupMemberRead(GroupMemberBase):
    student_id: ConstrainedId
    date_joined: datetime

class GroupMemberReadWithGroups(GroupMemberBase):
    group: "GroupRead"

class GroupMemberReadWithContent(GroupMemberBase):
    group: "GroupReadWithContent"

class GroupMemberUpdate(SQLModel):
    pass 



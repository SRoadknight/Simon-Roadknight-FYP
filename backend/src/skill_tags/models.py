from datetime import datetime
from typing import TYPE_CHECKING, Union
from sqlmodel import SQLModel, Field, Relationship, TIMESTAMP, Column, text, AutoString
from typing_extensions import Annotated, TypeAliasType
from annotated_types import Len

if TYPE_CHECKING:
    from src.students.models import StudentSkillTag
    from src.job_posts.models import JobPostSkillTag
    from src.job_profiles.models import JobProfileSkillTag
    from src.events.models import EventSkillTag
    from src.appointments.models import AppointmentSkillTag
    from src.content.models import ContentSkillTag


# Skills that can then be attached to students, jobs, events, and appointments
# I can look into having a single tag for all the reads (I don't think
# I can do it for the create and update models)
# Skills that can then be attached to students, jobs, events, and appointments
    
class AttachedSkillTagBase(SQLModel):
       pass


class AttachedSkillTagRead(AttachedSkillTagBase):
    skill: "SkillTagRead"


SkillName = TypeAliasType(
    'SkillName', 
    Annotated[str, Len(min_length=1, max_length=25)]
    )

SkillDescription = TypeAliasType(
    'SkillDescription', 
    Annotated[str, Len(min_length=0, max_length=100)]
    )

class SkillTagBase(SQLModel):
    name: SkillName = Field(max_length=25, sa_type=AutoString)
    
class SkillTag(SkillTagBase, table=True):
    __tablename__ = "skill_tag"
    id: Union[int, None] = Field(primary_key=True, default=None)
    last_used: Union[datetime, None] = Field(default=None, sa_column=Column(TIMESTAMP(timezone=True)),)
    date_added: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )

    students: list["StudentSkillTag"] = Relationship(back_populates="skill")
    job_posts: list["JobPostSkillTag"] = Relationship(back_populates="skill")
    events: list["EventSkillTag"] = Relationship(back_populates="skill")
    appointments: list["AppointmentSkillTag"] = Relationship(back_populates="skill")
    job_profiles: list["JobProfileSkillTag"] = Relationship(back_populates="skill")
    content: list["ContentSkillTag"] = Relationship(back_populates="skill")

class SkillTagCreate(SkillTagBase):
    pass

class SkillTagRead(SkillTagBase):
    pass

class SkillTagUpdate(SQLModel):
    name: Union[SkillName, None] = None
    description: Union[SkillDescription, None] = None
    active: Union[bool, None] = None
    last_used: Union[datetime, None] = None

    


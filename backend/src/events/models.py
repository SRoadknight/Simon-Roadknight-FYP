from datetime import datetime, date, time
from typing import TYPE_CHECKING, Union, Dict, Any
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, AutoString, Column, text, TIMESTAMP
from src.skill_tags.models import AttachedSkillTagBase, SkillTagRead
from src.skill_tags.models import SkillTag
from src.models import ConstrainedId, Name, Description
from src.students.models import StudentReadWithUser

if TYPE_CHECKING:
    from src.students.models import Student
    from src.skill_tags.models import SkillTag


class EventType(str, Enum):
    workshop = "workshop"
    hackathon = "hackathon"
    other = "other"


class EventStatus(str, Enum):
    UPCOMING = "upcoming"
    CANCELLED = "cancelled"
    COMPLETE = "complete"


class EventBase(SQLModel):
    name: Name = Field(max_length=50, sa_type=AutoString)
    description: Description = Field(max_length=250, sa_type=AutoString)
    event_type: EventType 
    event_start_time: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    event_end_time: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    event_location: str
    

class Event(EventBase, table=True):
    __tablename__ = "event"
    id: int = Field(primary_key=True, default=None)
   
    status: EventStatus = Field(default=EventStatus.UPCOMING)
    date_added: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )

    students: list["EventRegistration"] = Relationship(back_populates="event")
    skills: list["EventSkillTag"] = Relationship(back_populates="event")

class EventCreate(EventBase):
    skill_data: Union[list[Dict[str, Any]], None] = None

class EventRead(EventBase):
    id: int
    status: EventStatus

class EventReadWithSkills(EventRead):
     skills: list["EventSkillTagRead"] = []
    

class EventUpdate(SQLModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    event_type: Union[EventType, None] = None
    event_end_time: Union[datetime, None] = None
    event_start_time: Union[datetime, None] = None
    event_location: Union[str, None] = None
    status: Union[EventStatus, None] = None
   

# event registration
    
class EventRegistrationBase(SQLModel):
    pass 

class EventRegistration(EventRegistrationBase, table=True):
    __tablename__ = "event_registration"
    student_id: ConstrainedId = Field(
        foreign_key="student.id",
        primary_key=True, 
        sa_type=AutoString,
        index=True
        )
    event_id: int = Field(foreign_key="event.id", primary_key=True)
    registration_date: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )

    
    student: "Student" = Relationship(back_populates="events")
    event: "Event" = Relationship(back_populates="students")

class EventRegistrationCreate(EventRegistrationBase):
    pass

class EventRegistrationRead(EventRegistrationBase):
    event: EventRead

class EventRegistrationReadWithStudent(EventRegistrationBase):
    registration_date: datetime
    student: StudentReadWithUser


class EventSkillTagBase(SQLModel):
    pass

class EventSkillTag(EventSkillTagBase, table=True):
    __tablename__ = "event_skill_tags"
    event_id: int = Field(foreign_key="event.id",primary_key=True, index=True)
    skill_id: int = Field(foreign_key="skill_tag.id", primary_key=True, index=True)
    date_added: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )

    event: "Event" = Relationship(back_populates="skills")
    skill: "SkillTag" = Relationship(back_populates="events")


class EventSkillTagCreate(AttachedSkillTagBase):
    event_id: int
    skill_id: int

class EventSkillTagRead(EventSkillTagBase):
    date_added: datetime
    skill: SkillTagRead




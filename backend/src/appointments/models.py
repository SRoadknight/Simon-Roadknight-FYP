from datetime import datetime
from typing import TYPE_CHECKING, Union, Dict, Any
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, AutoString, Column, text, TIMESTAMP
from src.skill_tags.models import AttachedSkillTagBase, SkillTagRead
from src.models import Name, Description, ConstrainedId

if TYPE_CHECKING:
    from src.students.models import Student
    from src.skill_tags.models import SkillTag
    from src.staff.models import CareersStaff



class AppointmentType(str, Enum):
    group = "group"
    one_on_one = "one_on_one"
    other = "other"

class AppointmentStatus(str, Enum):
    available = "available"
    booked = "booked"
    cancelled = "cancelled"
    complete = "complete"


class AppointmentBase(SQLModel):
    name: Name = Field(max_length=50, sa_type=AutoString)
    description: Description = Field(max_length=250, sa_type=AutoString)
    type: AppointmentType = Field(default=AppointmentType.one_on_one)
    app_start_time: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)),)
    location: str
    

class Appointment(AppointmentBase, table=True):
    __tablename__ = "appointment"
    id: Union[int, None] = Field(primary_key=True, default=None)
    
    staff_id: ConstrainedId = Field(foreign_key="career_staff.id", sa_type=AutoString, index=True)
    app_end_time: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    status: AppointmentStatus = Field(default=AppointmentStatus.available)
   

    staff: "CareersStaff" = Relationship(back_populates="appointments")
    students: list["AppointmentBooking"] = Relationship(back_populates="appointment")
    skills: list["AppointmentSkillTag"] = Relationship(back_populates="appointment")


class AppointmentCreate(AppointmentBase):
    length_minutes: int
    skill_data: Union[list[Dict[str, Any]], None] = None

class AppointmentRead(AppointmentBase):
    id: int
    status: AppointmentStatus
    app_end_time: datetime

class AppointmenReadWithDetails(AppointmentRead):
    skills: Union[list["AppointmentSkillTagRead"], None] = None


class AppointmentUpdate(SQLModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    app_start_time: Union[datetime, None] = None
    length_minutes: Union[int, None] = None
    location: Union[str, None] = None
    type: Union[AppointmentType, None] = None
    status: Union[AppointmentStatus, None] = None
    app_end_time: datetime = None 



# appointment booking

class AppointmentBookingBase(SQLModel):
    pass 

class AppointmentBooking(AppointmentBookingBase, table=True):
    __tablename__ = "appointment_booking"
    appointment_id: int = Field(foreign_key="appointment.id", primary_key=True)
    student_id: ConstrainedId = Field(
        foreign_key="student.id",
        primary_key=True, 
        sa_type=AutoString,
        index=True
        )
    date_booked: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),)

    student: "Student" = Relationship(back_populates="appointments")
    appointment: "Appointment" = Relationship(back_populates="students")

class AppointmentBookingRead(AppointmentBookingBase):
    appointment: AppointmentRead

class AppointmentSkillTag(AttachedSkillTagBase, table=True):
    __tablename__ = "appointment_skill_tags"
    appointment_id: int = Field(foreign_key="appointment.id",primary_key=True)
    skill_id: int = Field(foreign_key="skill_tag.id", primary_key=True)

    appointment: "Appointment" = Relationship(back_populates="skills")
    skill: "SkillTag" = Relationship(back_populates="appointments")

class AppointmentSkillTagRead(AttachedSkillTagBase):
    skill: SkillTagRead

class AppointmentSkillTagCreate(AttachedSkillTagBase):
    appointment_id: int
    skill_id: int 
from datetime import date, time, datetime
from typing import TYPE_CHECKING, Union
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, AutoString, Column, text, TIMESTAMP
from src.models import ConstrainedId
from sqlalchemy import UniqueConstraint
from src.job_posts.models import JobPostRead, JobPostCreate
from src.students.models import StudentReadOnlyUser


if TYPE_CHECKING:
    from src.job_posts.models import JobPost
    from src.students.models import Student

# Applications

class JobApplicationStage(str, Enum):
    applied = "applied"
    interview = "interviewing"
    offer = "offer"
    accepted = "accepted"
    rejected = "rejected"

class JobApplicationBase(SQLModel):
    stage: JobApplicationStage = Field(default="applied")
    date_applied: Union[date, None] = Field(default=date.today(), index=True)
    careers_plus_assisted: bool = Field(default=False)
    notes: Union[str, None] = Field(default=None, max_length=500, sa_type=AutoString)

class JobApplication(JobApplicationBase, table=True):
    __tablename__ = "student_job_application"
    id: Union[int, None] = Field(primary_key=True, default=None)
    student_id: ConstrainedId = Field(
        foreign_key="student.id",
        sa_type=AutoString
        )
    job_post_id: int = Field(
        foreign_key="job_post.id"
        )
    

    __table_args__ = (
        UniqueConstraint('student_id', 'job_post_id', name='unique_student_job'),
    )

    job_post: "JobPost" = Relationship(back_populates="student_applications")
    student: "Student" = Relationship(back_populates="job_applications")
    activities: list["JobApplicationActivity"] = Relationship(back_populates="job_application")

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationRead(JobApplicationBase):
    id: int
    job_post_id: int
    student_id: ConstrainedId

class JobApplicationUpdate(SQLModel):
    stage: Union[JobApplicationStage, None] = None
    date_applied: Union[date, None] = None
    careers_plus_assisted: Union[bool, None] = None
    notes: Union[str, None] = None

class JobApplicationReadWithJob(JobApplicationRead):
    job_post: JobPostRead


class JobApplicationReadWithActivities(JobApplicationRead):
    activities: list["JobApplicationActivityRead"]

class JobApplicationReadWithActivitiesAndJob(JobApplicationReadWithActivities, JobApplicationReadWithJob):
    pass


class JobApplicationActivityType(str, Enum):
    intereview = "interview"
    phone_call = "phone_call"
    test = "test"
    assessment_center = "assessment_center"
    take_home_project = "take_home_project"
    follow_up = "follow_up"
    general_note = "general_note"
    other = "other"

# Job application activities 

class JobApplicationActivityBase(SQLModel):
    activity_date: Union[date, None] = Field(default=None)
    activity_time: Union[time, None] = Field(default=None)
    title: str = Field(sa_type=AutoString)
    activity_type: JobApplicationActivityType = Field(default="general_note")
    notes: Union[str, None] = Field(default=None, sa_type=AutoString)

class JobApplicationActivity(JobApplicationActivityBase, table=True):
    __tablename__ = "job_application_activity"

    id: int = Field(primary_key=True, default=None)
    job_application_id: int = Field(foreign_key="student_job_application.id")
    date_created: Union[datetime, None] = Field(
    default=None,
    sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )
    last_updated: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()"), 
        onupdate=text("now()")))
    

    job_application: JobApplication = Relationship(back_populates="activities")


class JobApplicationActivityCreate(JobApplicationActivityBase):
    pass

class JobApplicationActivityRead(JobApplicationActivityBase):
    id: int
    date_created: datetime


class JobApplicationActivityUpdate(SQLModel):
    activity_date: Union[date, None] = None 
    activity_time: Union[time, None] = None
    title: Union[str, None] = None
    activity_type: Union[JobApplicationActivityType, None] = None
    notes: Union[str, None] = None
    # The below could be used if the activity was linked to the wrong job application
    # job_application_id: Union[int, None] = None


class StudentJobPostApplicationCreate(JobPostCreate, JobApplicationCreate):
    pass

class JobApplicationReadWithStudent(JobApplicationRead):
    student: StudentReadOnlyUser


class JobApplicationActivityReadFull(JobApplicationActivityRead):
    job_application: JobApplicationReadWithStudent


class JobApplicationReadFull(JobApplicationRead):
    student: StudentReadOnlyUser
    activities: list[JobApplicationActivityReadFull]
    job_post: JobPostRead

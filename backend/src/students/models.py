from datetime import datetime 
from typing import TYPE_CHECKING, Union
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, AutoString, Column, text, TIMESTAMP
from src.models import ConstrainedId, Name, Description, LongDescription
from src.auth.models import UserCreateForStudents, UserRead
from src.job_posts.models import JobPost, JobPostRead
from src.degrees.models import Degree, DegreeRead
from src.skill_tags.models import AttachedSkillTagBase
from pydantic import field_validator
from src.utils import validate_website_url
from src.job_posts.models import JobPostRead
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from src.auth.models import User
    from src.appointments.models import AppointmentBooking
    from src.applications.models import JobApplication
    from src.interactions.models import Interaction
    from src.events.models import EventRegistration
    from src.groups.models import GroupMember
    from src.job_posts.models import JobPost, SavedJobPost
    from src.degrees.models import Degree
    from src.skill_tags.models import SkillTag
   

# Copy of level taught from the degree model -- these can use the same one in the future
class LevelOfStudy(str, Enum):
    FOUNDATION = "Foundation"
    UNDERGRADUATE = "Undergraduate"
    POSTGRADUATE = "Postgraduate"
    PHD = "PhD"

# Current student employment status to know if they are in related work etc 
class CurrentEmploymentStatus(str, Enum):
    UNEMPLOYED = "unemployed"
    CASUAL_WORK = "casual_work"
    RELATED_WORK = "related_work"
    RELATED_WORK_GRADUATE = "related_work_graduate"
    GRADUATE_SCHEME = "graduate_scheme"
    GRADUATE_LEVEL_WORK = "graduate_level_work"
    INTERNSHIP = "internship"
    PLACEMENT_YEAR = "placement_year"
    SELF_EMPLOYED = "self_employed"
    OTHER = "other"


# Confidence level - can be used in multiple fields
class ConfidenceLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"




class StudentBase(SQLModel):
    id: ConstrainedId = Field(primary_key=True, sa_type=AutoString)
    current_employment_status: Union[CurrentEmploymentStatus, None] = Field(default=None)
    placement_year: bool = Field(default=False)
    related_work_experience: bool = Field(default=False)
    internship_experience: bool = Field(default=False)
    casual_work_experience: bool = Field(default=False)
    extra_caricular_activities: bool = Field(default=False)
    other_academic_info: Union[str, None] = Field(default=None)
    about: Union[LongDescription, None] = Field(default=None, sa_type=AutoString)
    career_confidence_level: Union[ConfidenceLevel, None] = Field(default=None)
    career_options_confidence_level: Union[ConfidenceLevel, None] = Field(default=None)


class Student(StudentBase, table=True):
    user_id: int = Field(foreign_key="app_user.id", index=True)
    current_student: bool = Field(default=True)
    graduated: bool = Field(default=False)

    last_updated: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()"), 
        onupdate=text("now()")))
    
    

    user: "User" = Relationship(back_populates="student")
    external_profiles: list["ExternalProfile"] = Relationship(back_populates="student")
    appointments: list["AppointmentBooking"] = Relationship(back_populates="student")
    events: list["EventRegistration"] = Relationship(back_populates="student")
    job_applications: list["JobApplication"] = Relationship(back_populates="student")
    staff_interactions: list["Interaction"] = Relationship(back_populates="student")
    skills: list["StudentSkillTag"] = Relationship(back_populates="student")
    groups: list["GroupMember"] = Relationship(back_populates="student")
    job_posts: list["StudentJobPost"] = Relationship(back_populates="student")
    degrees: list["StudentDegree"] = Relationship(back_populates="student")
    keywords: list["StudentKeyword"] = Relationship(back_populates="student")
    activities: list["StudentActivity"] = Relationship(back_populates="student")
    saved_job_posts: list["SavedJobPost"] = Relationship(back_populates="student")

class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    pass

class StudentReadWithUser(StudentRead):
    user: UserRead

class StudentUpdate(SQLModel):
    current_employment_status: Union[CurrentEmploymentStatus, None] = None
    related_work_experience: bool = False
    internship_experience: bool = False
    casual_work_experience: bool = False
    extra_caricular_activities: bool = False
    other_academic_info: Union[str, None] = None
    about: Union[LongDescription, None] = None
    career_confidence_level: Union[ConfidenceLevel, None] = None
    career_options_confidence_level: Union[ConfidenceLevel, None] = None


# create a user and student at the same time
class StudentUserCreate(UserCreateForStudents, StudentCreate):
    pass

class StudentReadWithUser(StudentRead):
    user: UserRead

class StudentReadOnlyUser(SQLModel):
    user: UserRead



# Degrees a student has studied or is studying with current institution
    
# enum for degree grades 
class DegreeGrade(str, Enum):
    FIRST = "First"
    TWO_ONE = "2:1"
    TWO_TWO = "2:2"
    THIRD = "Third"


class StudentDegreeBase(SQLModel):
    pass

class StudentDegree(StudentDegreeBase, table=True):
    __tablename__ = "student_degree"
    student_id: ConstrainedId = Field(foreign_key="student.id", primary_key=True, sa_type=AutoString)
    degree_code: str = Field(foreign_key="degree.degree_code", primary_key=True)

    graduated: bool = Field(default=False)
    grade_awarded: Union[DegreeGrade, None] = Field(default=None)
    graduation_year: Union[int, None] = Field(default=None)

    student: Student = Relationship(back_populates="degrees")
    degree: "Degree" = Relationship(back_populates="students")

class StudentDegreeCreate(StudentDegreeBase):
    pass
    

class StudentDegreeRead(StudentDegreeBase):
    degree_code: str
    graduated: bool = Field(default=False)
    grade_awarded: Union[DegreeGrade, None] = Field(default=None)
    graduation_year: Union[int, None] = Field(default=None)

    degree: DegreeRead

class StudentDegreeUpdate(SQLModel):
    pass


# Placing other models here that are related to the student model
# usually with a one to many relationship with student 

class ExternalWebsite(str, Enum):
    linkedin = "linkedin"
    github = "github"
    x = "x"
    other = "other"

class ExternalProfileBase(SQLModel):
    website: ExternalWebsite 
    website_url: str 

    _validate_website_url = field_validator("website_url")(validate_website_url)

class ExternalProfile(ExternalProfileBase, table=True):
    __tablename__ = "external_profile"
    id: int = Field(primary_key=True, default=None)
    student_id: ConstrainedId = Field(foreign_key="student.id", sa_type=AutoString)

    __table_args__ = (
        UniqueConstraint('student_id', 'website', name='unique_student_website'),
    )

    student: "Student" = Relationship(back_populates="external_profiles")

class ExternalProfileCreate(ExternalProfileBase):
    pass

class ExternalProfileRead(ExternalProfileBase):
    pass

class ExternalProfileUpdate(SQLModel):
    website: Union[ExternalWebsite, None] = None
    website_url: Union[str, None] = None

    _validate_website_url = field_validator("website_url")(validate_website_url)


# Student skill tags

class StudentSkillTag(AttachedSkillTagBase, table=True):
    __tablename__ = "student_skill_tags"
    student_id: ConstrainedId = Field(foreign_key="student.id",primary_key=True, sa_type=AutoString)
    skill_id: int = Field(foreign_key="skill_tag.id", primary_key=True)
 

    student: "Student" = Relationship(back_populates="skills")
    skill: "SkillTag" = Relationship(back_populates="students")


class StudentSkillTagCreate(AttachedSkillTagBase):
    skill_id: int = Field(foreign_key="skill_tag.id", primary_key=True)

class StudentSkillTagUpdate(AttachedSkillTagBase):
    pass


# Student job post to then be used in the job application
class StudentJobPostBase(SQLModel):
    pass

class StudentJobPost(StudentJobPostBase, table=True):
    __tablename__ = "student_job_post"
    student_id: ConstrainedId = Field(foreign_key="student.id", primary_key=True, sa_type=AutoString)
    job_post_id: int = Field(foreign_key="job_post.id", primary_key=True)

    student: Student = Relationship(back_populates="job_posts")
    job_post: JobPost = Relationship(back_populates="students_posts")


class StudentJobPostCreate(StudentJobPostBase):
    student_id: ConstrainedId 
    job_post_id: int 

class StudentJobPostRead(StudentJobPostBase):
    job_post: JobPostRead



class StudentKeywordBase(SQLModel):
    keyword: str = Field(max_length=100)

class StudentKeyword(StudentKeywordBase, table=True):
    __tablename__ = "student_keyword"
    id: Union[int, None] = Field(primary_key=True, default=None)
    student_id: ConstrainedId = Field(foreign_key="student.id", sa_type=AutoString)

    student: "Student" = Relationship(back_populates="keywords")

class StudentKeywordCreate(StudentKeywordBase):
    student_id: ConstrainedId

class StudentKeywordRead(StudentKeywordBase):
    pass

class StudentKeywordUpdate(SQLModel):
    keyword: str = Field(max_length=100)



# Student activities

class ActivityType(str, Enum):
    CV_REVIEW = "cv_review"
    MOCK_INTERVIEW = "mock_interview"
    NETWORKING = "networking"
    JOB_SEARCH = "job_search"
    APPLICATION_SUPPORT = "application_support"
    CAREER_DEVELOPMENT = "career_development"
    PSYCHOMETRIC_TEST_PRACTICE = "psychometric_test_practice"
    ASESSMENT_CENTRE_PRACTICE = "assessment_centre_practice"
    OTHER = "other"

class StudentActivityBase(SQLModel):
    title: Name = Field(min_length=3, max_length=50, sa_type=AutoString)
    activity_type: ActivityType
    description: Description = Field(min_length=3, max_length=250, sa_type=AutoString)
    activity_date: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )


class StudentActivity(StudentActivityBase, table=True):
    __tablename__ = "student_activities"
    id: Union[int, None] = Field(primary_key=True, default=None)
    student_id: ConstrainedId = Field(foreign_key="student.id", sa_type=AutoString)

    student: "Student" = Relationship(back_populates="activities")


class StudentActivityCreate(StudentActivityBase):
    pass

class StudentActivityRead(StudentActivityBase):
    id: int

class StudentActivityUpdate(SQLModel):
    title: Union[Name, None] = None
    activity_type: Union[ActivityType, None] = None
    description: Union[Description, None] = None
    activity_date: Union[datetime, None] = None




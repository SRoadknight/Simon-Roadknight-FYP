from datetime import date
from typing import TYPE_CHECKING, Union, Dict, Any
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, AutoString 
from src.skill_tags.models import AttachedSkillTagBase
from src.models import Name
from pydantic import field_validator 
from src.utils import validate_website_url
from src.skill_tags.models import SkillTag
from sqlalchemy import UniqueConstraint
from src.models import ConstrainedId



if TYPE_CHECKING:
    from src.students.models import StudentJobPost, Student
    from src.skill_tags.models import SkillTag
    from src.companies.models import CompanyJobPost
    from src.applications.models import JobApplication
    


# enum for job source 
class JobSource(str, Enum):
    STAFF = "staff"
    COMPANY = "company"
    STUDENT = "student" # This will be for jobs that students find themselves and not visibile to others
    EXTERNAL = "external" # This will be for jobs that are scraped from external websites
    
# enum for job post status
class JobPostStatus(str, Enum):
    ONGOING = "ongoing"
    CLOSED = "closed"
    REMOVED = "removed"

class JobType(str, Enum):
    PLACEMENT_INTERNSHIP = "placement/internship"
    GRADUATE_JOB = "graduate"

# enum for degree required attainment
class DegreeRequired(str, Enum):
    ALL_GRADES = "All grades"
    TWO_TWO = "2:2 and above"
    TWO_ONE = "2:1 and above"
    FIRST = "First"
    MASTERS = "Master's and above"
    TWO_TWO_EXPECTED = "2:2 and above (expected)"
    TWO_ONE_EXPECTED = "2:1 and above (expected)"
    FIRST_EXPECTED = "First (expected)"

#  visibility enum for future use, for now it will only be used for student job posts (only visible to the student)
class Visibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"

class JobPostBase(SQLModel):
    title: Name = Field(sa_type=AutoString, index=True)
    company_name: Name = Field(sa_type=AutoString)
    description: str 
    location: str = Field(max_length=100)
    salary: Union[str, None] = Field(default=None)
    job_type: JobType = Field(default="graduate")
    hiring_mutiple_candidates: bool = Field(default=False)
    degree_required: DegreeRequired 
    # posting_date: str = Field(default=None) # The scraped jobs don't have a date so I need to consider this 
    # Deadline needs changing to a date format based on what pre-processing is done to the scraped jobs -- Some are just ongoing so this can also be null
    deadline: Union[date, None] = Field(default=None) # This will be used for student job posts
    website_url: Union[str, None] = Field(default=None)
    status: JobPostStatus = Field(default="ongoing")

    _validate_job_url = field_validator("website_url")(validate_website_url)
    

class JobPost(JobPostBase, table=True):
    __tablename__ = "job_post"
    id: Union[int, None] = Field(primary_key=True, default=None)
    source: JobSource 
    visibility: Visibility = Field(default="private") # This will be used for student job posts
    
    
    skills: list["JobPostSkillTag"] = Relationship(back_populates="job_post")
    students_posts: list["StudentJobPost"] = Relationship(back_populates="job_post")
    company_posts: list["CompanyJobPost"] = Relationship(back_populates="job_post")
    student_applications: list["JobApplication"] = Relationship(back_populates="job_post")
    keywords: list["JobPostKeyword"] = Relationship(back_populates="job_post")
    saved_by: list["SavedJobPost"] = Relationship(back_populates="job_post")

    
    
class JobPostCreate(JobPostBase): 
    skill_data: Union[list[Dict[str, Any]], None] = None

class JobPostRead(JobPostBase):
    id: int

class JobPostReadWithSkills(JobPostRead):
    skills: list["SkillTag"] = []

class JobPostUpdate(SQLModel):
    title: Union[Name, None] = None
    company_name: Union[Name, None] = None
    description: Union[str, None] = None
    location: Union[str, None] = None
    salary: Union[str, None] = None
    job_type: Union[JobType, None] = None
    hiring_mutiple_candidates: Union[bool, None] = None
    degree_required: Union[DegreeRequired, None] = None
    deadline: Union[date, None] = None
    website_url: Union[str, None] = None
    status: Union[JobPostStatus, None] = None
    
    _validate_job_url = field_validator("website_url")(validate_website_url)



class JobPostSkillTag(AttachedSkillTagBase, table=True):
    __tablename__ = "job_post_skill_tags"
    job_post_id: int = Field(foreign_key="job_post.id", primary_key=True)
    skill_id: int = Field(foreign_key="skill_tag.id", primary_key=True)
    

    job_post: "JobPost" = Relationship(back_populates="skills")
    skill: "SkillTag" = Relationship(back_populates="job_posts")


class JobPostSkillTagCreate(AttachedSkillTagBase):
    job_post_id: int 
    skill_id: int



class JobPostKeywordBase(SQLModel):
    keyword: str = Field(max_length=100)


class JobPostKeyword(JobPostKeywordBase, table=True):
    __tablename__ = "job_post_keyword"
    id: Union[int, None] = Field(primary_key=True, default=None)
    job_post_id: int = Field(foreign_key="job_post.id")
    
    job_post: "JobPost" = Relationship(back_populates="keywords")

class JobPostKeywordCreate(JobPostKeywordBase):
    job_post_id: int

class JobPostKeywordRead(JobPostKeywordBase):
    pass

class JobPostKeywordUpdate(SQLModel):
    keyword: Union[str, None] = None


class SavedJobPostBase(SQLModel):
    job_post_id: int = Field(foreign_key="job_post.id", primary_key=True)
    student_id: ConstrainedId = Field(foreign_key="student.id", primary_key=True, sa_type=AutoString)

class SavedJobPost(SavedJobPostBase, table=True):
    __tablename__ = "saved_job_post"
    

    __table_args__ = (
        UniqueConstraint('student_id', 'job_post_id', name='unique_job_saved'),
    )

    
    job_post: "JobPost" = Relationship(back_populates="saved_by")
    student: "Student" = Relationship(back_populates="saved_job_posts")

class SavedJobPostCreate(SavedJobPostBase):
    pass

class SavedJobPostRead(SavedJobPostBase):
    job_post: JobPostRead





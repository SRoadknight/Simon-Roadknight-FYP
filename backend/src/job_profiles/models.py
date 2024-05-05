from datetime import datetime
from typing import TYPE_CHECKING, Union
from sqlmodel import SQLModel, Field, Relationship, AutoString, Column, TIMESTAMP, text
from src.skill_tags.models import SkillTagRead
from src.degrees.models import DegreeRead
from annotated_types import Len
from typing_extensions import Annotated, TypeAliasType
from pydantic import field_validator
from src.utils import validate_website_url
from typing import Any, Dict

if TYPE_CHECKING:
    from src.skill_tags.models import SkillTag 
    from src.degrees.models import Degree


JobProfileTitle = TypeAliasType(
    'JobProfileTitle', 
    Annotated[str, Len(min_length=1, max_length=25)]
    )

JobProfileMiniDescription = TypeAliasType(
    'JobProfileMiniDescription',
    Annotated[str, Len(min_length=0, max_length=100)]
    )


class JobProfileBase(SQLModel):
    title: JobProfileTitle = Field(max_length=25, sa_type=AutoString)
    mini_description: JobProfileMiniDescription = Field(max_length=100, sa_type=AutoString)
    website_url: Union[str, None] = Field(default=None)

    _validate_job_profile_url = field_validator("website_url")(validate_website_url)
    

class JobProfile(JobProfileBase, table=True):
    __tablename__ = "job_profile"
    id: Union[int, None] = Field(primary_key=True, default=None)
    is_active: bool = Field(default=True)

    skills: list["JobProfileSkillTag"] = Relationship(back_populates="job_profile")
    degrees: list["JobProfileDegree"] = Relationship(back_populates="job_profile")

class JobProfileCreate(JobProfileBase):
    skill_data: Union[list[Dict[str, Any]], None] = None

class JobProfileRead(JobProfileBase):
    is_active: bool

class JobProfileUpdate(SQLModel):
    title: Union[JobProfileTitle, None] = None 
    mini_description: Union[JobProfileMiniDescription, None] = None 
    website_url: Union[str, None] = None 
    active: Union[bool, None] = None

    _validate_company_url = field_validator("website_url")(validate_website_url)



class JobProfileSkillTagBase(SQLModel):
    weight: float = Field(default=1, ge=0, le=1)

class JobProfileSkillTag(JobProfileSkillTagBase, table=True):
    __tablename__ = "job_profile_skill_tags"
    job_profile_id: int = Field(foreign_key="job_profile.id", primary_key=True)
    skill_id: int = Field(foreign_key="skill_tag.id", primary_key=True)
    date_added: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )

    job_profile: "JobProfile" = Relationship(back_populates="skills")
    skill: "SkillTag" = Relationship(back_populates="job_profiles")

class JobProfileSkillTagRead(JobProfileSkillTagBase):
    skill: "SkillTagRead"

class JobProfileSkillTagCreate(JobProfileSkillTagBase):
    pass

class JobProfileSkillTagUpdate(SQLModel):
    pass


# add degrees to job profiles
class JobProfileDegreeBase(SQLModel):
    pass

class JobProfileDegree(JobProfileDegreeBase, table=True):
    __tablename__ = "job_profile_degree"
    job_profile_id: int = Field(foreign_key="job_profile.id", primary_key=True)
    degree_code: str = Field(foreign_key="degree.degree_code", primary_key=True)

    job_profile: JobProfile = Relationship(back_populates="degrees")
    degree: "Degree" = Relationship(back_populates="job_profiles")

class JobProfileDegreeCreate(JobProfileDegreeBase):
    job_profile_id: int
    degree_code: str

class JobProfileDegreeRead(JobProfileDegreeBase):
    degree: "DegreeRead"

class JobProfileDegreeUpdate(SQLModel):
    pass




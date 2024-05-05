from typing import TYPE_CHECKING, Union
from sqlmodel import SQLModel, Field, Relationship, AutoString
from src.models import ConstrainedId
from ..auth.models import UserCreateForCompany, UserRead
from ..job_posts.models import JobPost, JobPostRead
from src.models import ConstrainedId, Name, Description
from pydantic import validator
from src.utils import validate_website_url

if TYPE_CHECKING:
    from src.auth.models import User 
    from src.job_posts.models import JobPost




class CompanyBase(SQLModel):
    name: Name = Field(sa_type=AutoString)
    description: Description = Field(sa_type=AutoString)
    website_url: str 

    _validate_company_url = validator("website_url", allow_reuse=True)(validate_website_url)
    

class Company(CompanyBase, table=True):
    id: ConstrainedId = Field(primary_key=True, sa_type=AutoString)
    user_id: int = Field(foreign_key="app_user.id", index=True)

    user: "User" = Relationship(back_populates="company")
    job_posts: list["CompanyJobPost"] = Relationship(back_populates="company")

class CompanyCreate(CompanyBase):
    id: ConstrainedId

class CompanyRead(CompanyBase):
    pass 

class CompanyUpdate(SQLModel):
    name: Union[Name, None] = None
    description: Union[Description, None] = None
    website_url: Union[str, None] = None

    _validate_company_url = validator("website_url", allow_reuse=True)(validate_website_url)

class CompanyUpdateAdmin(CompanyUpdate):
    company_id: ConstrainedId
    

class CompanyUserCreate(UserCreateForCompany, CompanyCreate):
    pass

class CompanyReadWithUser(CompanyRead):
    user: UserRead



class CompanyJobPostBase(SQLModel):
    pass

class CompanyJobPost(CompanyJobPostBase, table=True):
    __tablename__ = "company_job_post"
    company_id: ConstrainedId = Field(foreign_key="company.id", primary_key=True, sa_type=AutoString)
    job_post_id: int = Field(foreign_key="job_post.id", primary_key=True)

    company: Company = Relationship(back_populates="job_posts")
    job_post: JobPost = Relationship(back_populates="company_posts")

class CompanyJobPostCreate(CompanyJobPostBase):
    company_id: ConstrainedId
    job_post_id: int

class CompanyJobPostRead(CompanyJobPostBase):
    job_post: JobPostRead

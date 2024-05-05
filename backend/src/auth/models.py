from datetime import datetime
from typing import TYPE_CHECKING, Union
from typing_extensions import Annotated, TypeAliasType
from annotated_types import Len
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, AutoString, Column, TIMESTAMP, text
from pydantic import EmailStr
from sqlalchemy.sql import func
from src.models import ConstrainedId
from pydantic import field_validator

if TYPE_CHECKING:
    from src.students.models import Student
    from src.staff.models import CareersStaff
    from src.companies.models import Company


class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    sub: EmailStr
    user_id: Union[int, None] = None
    user_type: Union["UserType", None] = None
    disabled: Union[bool, None] = None
    related_entity_id: Union[ConstrainedId, None] = None

class UserType(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    STUDENT = "student"
    COMPANY = "company"

ConstrainedHash = TypeAliasType(
    'HashedPassword', 
    Annotated[str, Len(min_length=60, max_length=60)]
    )


class UserBase(SQLModel):
    pass 

class User(UserBase, table=True):
    __tablename__ = "app_user"
    id: Union[int, None] = Field(primary_key=True, default=None)
    email_address: EmailStr = Field(sa_type=AutoString, unique=True, index=True)
    first_name: Union[str, None] = Field(default=None)
    last_name: Union[str, None] = Field(default=None)
   
    user_type: UserType
    disabled: bool = Field(default=False)
    hashed_password: ConstrainedHash = Field(
        default="$2a$12$04gLwzN/j2V8M.JhPE8sa.n7L96eV7pmCRGEy2pyFprD0mm1U0L8O", 
        sa_type=AutoString
        )
    date_created: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")),
    )
    last_updated: Union[datetime, None] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), onupdate=func.now()),
    )

    student: "Student" = Relationship(back_populates="user")
    careers_staff: "CareersStaff" = Relationship(back_populates="user")
    company: "Company" = Relationship(back_populates="user")


class UserCreate(UserBase):
    pass

class UserCreateForStudentsAndStaff(UserCreate):
    first_name: str
    last_name: str

class UserCreateForStaff(UserCreateForStudentsAndStaff):
    email_address: EmailStr

    @field_validator("email_address")
    def validate_staff_email(cls, value):
        if not value.endswith("@bcu.ac.uk"):
            raise ValueError("Staff email must end with @bcu.ac.uk")
        return value

class UserCreateForStudents(UserCreateForStudentsAndStaff):
    email_address: EmailStr

    @field_validator("email_address")
    def validate_student_email(cls, value):
        if not value.endswith("@mail.bcu.ac.uk"):
            raise ValueError("Student email must end with @mail.bcu.ac.uk")
        return value

class UserCreateForCompany(UserCreate):
    pass

class UserRead(UserBase):
    first_name: Union[str, None] 
    last_name: Union[str, None] 
    email_address: EmailStr

class UserUpdate(UserBase):
    pass
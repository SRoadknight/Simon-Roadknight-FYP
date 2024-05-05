from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, AutoString
from src.models import Name, Description
from typing import Union



if TYPE_CHECKING:
    from src.schools_departments.models import SchoolDepartment

class FacultyBase(SQLModel):
    faculty_name: Name = Field(sa_type=AutoString)
    faculty_description: Description = Field(sa_type=AutoString)

class Faculty(FacultyBase, table=True):
    __tablename__ = "faculty"
    id: Union[int, None] = Field(primary_key=True, default=None)

    schools_departments: list["SchoolDepartment"] = Relationship(back_populates="faculty")

class FacultyRead(FacultyBase):
    pass


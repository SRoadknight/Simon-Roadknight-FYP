from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from src.faculties.models import Faculty
    from src.degrees.models import Degree

class SchoolDepartmentBase(SQLModel):
    school_deparment_name: str
    school_deparment_description: str
    

class SchoolDepartment(SchoolDepartmentBase, table=True):
    __tablename__ = "school_department"
    id: int = Field(primary_key=True, default=None)
    faculty_id: int = Field(foreign_key="faculty.id", index=True)

    faculty: "Faculty" = Relationship(back_populates="schools_departments")
    degrees: list["Degree"] = Relationship(back_populates="school_department")

class SchoolDepartmentRead(SchoolDepartmentBase):
    pass

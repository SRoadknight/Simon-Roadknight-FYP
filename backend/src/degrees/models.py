from typing import TYPE_CHECKING, Union
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, AutoString 
from src.models import Name


if TYPE_CHECKING:
    from src.schools_departments.models import SchoolDepartment
    from src.students.models import StudentDegree
    from src.job_profiles.models import JobProfileDegree
    
class LevelTaught(str, Enum):
    FOUNDATION = "Foundation"
    UNDERGRADUATE = "Undergraduate"
    POSTGRADUATE = "Postgraduate"
    PHD = "PhD"
    
class DegreeBase(SQLModel):
    degree_code: str = Field(primary_key=True)
    degree_name: Name = Field(max_length=50, sa_type=AutoString)
    degree_level: LevelTaught

class Degree(DegreeBase, table=True):
    __tablename__ = "degree"
    school_deparment_id: int = Field(foreign_key="school_department.id", index=True)

    school_department: "SchoolDepartment" = Relationship(back_populates="degrees")
    students: list["StudentDegree"] = Relationship(back_populates="degree")
    job_profiles: Union["JobProfileDegree", None] = Relationship(back_populates="degree")



class DegreeRead(DegreeBase):
    pass 

class DegreeReadWithStudents(DegreeRead):
    students: list["StudentDegree"]


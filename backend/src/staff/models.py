from typing import TYPE_CHECKING, Union
from sqlmodel import SQLModel, Field, Relationship, AutoString 
from src.models import ConstrainedId
from ..auth.models import UserCreate, UserRead

if TYPE_CHECKING:
    from src.auth.models import User
    from src.interactions.models import Interaction
    from src.appointments.models import Appointment

class CareersStaffBase(SQLModel):
    job_title: str
    about: str

class CareersStaff(CareersStaffBase, table=True):
    __tablename__ = "career_staff"
    user_id: int = Field(foreign_key="app_user.id", index=True)
    id: ConstrainedId = Field(primary_key=True, sa_type=AutoString)


    user: "User" = Relationship(back_populates="careers_staff")
    appointments: list["Appointment"] = Relationship(
        back_populates="staff")
    student_interactions: list["Interaction"] = Relationship(
        back_populates="careers_staff")

    
class CareersStaffCreate(CareersStaffBase):
    id: ConstrainedId

class CareersStaffRead(CareersStaffBase):
    id: ConstrainedId

class CareersStaffReadWithUser(CareersStaffRead):
    user: UserRead

class CareersStaffUpdate(SQLModel):
    job_title: Union[str, None] = None
    about: Union[str, None] = None
    
class CareersStaffUserCreate(UserCreate, CareersStaffCreate):
    pass

class CareersStaffReadOnlyUser(SQLModel):
    user: UserRead
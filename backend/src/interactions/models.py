from datetime import date
from typing import TYPE_CHECKING, Union
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, AutoString 
from src.models import ConstrainedId, Name
from src.staff.models import CareersStaffReadOnlyUser
from src.students.models import StudentReadOnlyUser

if TYPE_CHECKING:
    from src.students.models import Student
    from src.staff.models import CareersStaff

# Interactions between students and careers staff


# Enum for the type of interaction that isn't monitored within this system
class InteractionType(str, Enum):
    EMAIL = "Email"
    MS_TEAMS = "MS_Teams"
    OTHER = "Other"

# Enum for the rating of the interaction
class EmojiRating(str, Enum):
    VERY_POOR = "😢"
    POOR = "😟"
    NEUTRAL = "😐"
    GOOD = "🙂"
    VERY_GOOD = "😀"


class InteractionBase(SQLModel):
    student_id: ConstrainedId = Field(foreign_key="student.id", sa_type=AutoString, index=True)
    title: Name = Field(max_length=50, sa_type=AutoString)
    interaction_date: Union[date, None] = Field(default=date.today(), index=True)
    type: InteractionType
    staff_notes: Union[str, None] = Field(default=None)
    

class Interaction(InteractionBase, table=True):
    __tablename__ = "interaction"
    id: int = Field(primary_key=True, default=None)
    careers_staff_id: ConstrainedId = Field(
        foreign_key="career_staff.id", sa_type=AutoString, index=True
        )
    helpful: Union[str, None] = Field(default=None)
    further_support: Union[str, None] = Field(default=None)
    emoji_rating: Union[EmojiRating, None] = Field(default=None)
    updated_by_student: Union[bool, None] = Field(default=False)
    

    student: "Student" = Relationship(back_populates="staff_interactions")
    careers_staff: "CareersStaff" = Relationship(back_populates="student_interactions")
   

    
class InteractionCreate(InteractionBase):
    pass 
    
class InteractionRead(InteractionBase):
    id: int
    careers_staff_id: ConstrainedId
    student_id: ConstrainedId
    helpful: Union[str, None] 
    further_support: Union[str, None]
    emoji_rating: Union[EmojiRating, None] 
    updated_by_student: Union[bool, None]
    

class StaffInteractionUpdate(SQLModel):
    title: Union[Name, None] = None
    interaction_date: Union[date, None] = None
    type: Union[InteractionType, None] = None
    staff_notes: Union[str, None] = None
    careers_staff_id: Union[ConstrainedId, None] = None
    length: Union[int, None] = None

class StudentInteractionUpdate(SQLModel):
    helpful: Union[str, None] = None
    further_support: Union[str, None] = None
    emoji_rating: Union[EmojiRating, None] = None

class InteractionReadWithStaff(InteractionRead):
    careers_staff: CareersStaffReadOnlyUser


class InteractionReadWithStudent(InteractionRead):
    student: StudentReadOnlyUser

class InteractionReadWithStudentAndStaff(InteractionRead):
    student: StudentReadOnlyUser 
    careers_staff:CareersStaffReadOnlyUser

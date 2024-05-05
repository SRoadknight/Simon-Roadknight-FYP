from typing import Dict, Type 
from src.auth.models import UserType, SQLModel
from src.students.models import Student
from src.companies.models import Company
from src.staff.models import CareersStaff

model_mapping: Dict[UserType, Type[SQLModel]] = {
    UserType.STUDENT: Student,
    UserType.COMPANY: Company,
    UserType.STAFF: CareersStaff
}


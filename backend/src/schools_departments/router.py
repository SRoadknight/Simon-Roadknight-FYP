from fastapi import APIRouter, Depends

from src.database import get_session
from src.auth.dependencies import get_current_active_user
from src.schools_departments import service
from src.schools_departments.models import SchoolDepartmentRead

router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Get all schools and departments
@router.get("", response_model=list[SchoolDepartmentRead])
async def read_schools_departments(session = Depends(get_session)):
    return await service.get_schools_departments(session=session)

# get a single school or department
@router.get("/{school_department_id}", response_model=SchoolDepartmentRead)
async def read_school_department(
    school_department_id: int,
    session = Depends(get_session)
    ):
    return await service.get_school_department_by_id(
        school_department_id=school_department_id,
        session=session
    )
    

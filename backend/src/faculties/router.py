from fastapi import APIRouter, Depends
from src.database import get_session

from src.auth.dependencies import get_current_active_user
from src.faculties import service
from src.faculties.models import FacultyRead

router = APIRouter(dependencies=[Depends(get_current_active_user)])


# Get all faculties
@router.get("", response_model=list[FacultyRead])
async def read_faculties(session = Depends(get_session)):
    faculties = await service.get_faculties(session=session)
    return faculties

# Get a single faculty
@router.get("/{faculty_id}", response_model=FacultyRead)
async def read_faculty(faculty_id: int, session = Depends(get_session)):
    return await service.get_faculty_by_id(faculty_id=faculty_id, session=session)
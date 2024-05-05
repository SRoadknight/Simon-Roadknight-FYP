from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import joinedload, selectinload

from src.faculties.exceptions import FacultyNotFound
from src.faculties.models import Faculty
from src.schools_departments.models import SchoolDepartment

async def get_faculties(session: AsyncSession):
   # get faculty with school departments
    result = await session.exec(
        select(Faculty)
        .options(selectinload(Faculty.schools_departments)
                 .joinedload(SchoolDepartment.degrees))
    )
    faculties = result.all()
    return faculties

async def get_faculty_by_id(faculty_id: int, session: AsyncSession):
    result = await session.exec(
        select(Faculty)
        .options(selectinload(Faculty.schools_departments))
        .where(Faculty.id == faculty_id)
    )
    faculty = result.first()
    if faculty is None:
        raise FacultyNotFound
    return faculty
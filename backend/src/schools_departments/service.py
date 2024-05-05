from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.schools_departments.exceptions import SchoolDepartmentNotFound
from src.schools_departments.models import SchoolDepartment


async def get_schools_departments(session: AsyncSession):
    result = await session.exec(select(SchoolDepartment))
    schools_departments = result.all()
    return schools_departments

async def get_school_department_by_id(school_department_id: int, session: AsyncSession):
    result = await session.exec(
        select(SchoolDepartment)
        .where(SchoolDepartment.id == school_department_id)
    )
    school_department = result.first()
    if school_department is None:
        raise SchoolDepartmentNotFound
    return school_department
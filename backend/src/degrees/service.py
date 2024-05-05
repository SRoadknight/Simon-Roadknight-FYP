from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.degrees.models import Degree
from src.degrees.exceptions import DegreeNotFound

async def get_degree_by_code(degree_code: str, session: AsyncSession):
    result = await session.exec(
        select(Degree).where(Degree.degree_code == degree_code)
    )
    degree = result.first()
    if degree is None:
        raise DegreeNotFound()
    return degree

async def get_degrees(session: AsyncSession):
    result = await session.exec(select(Degree))
    return result.all()
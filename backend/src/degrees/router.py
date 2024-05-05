from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import get_current_active_user

from src.degrees import service
from src.database import get_session
from src.degrees.models import DegreeRead


router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Get all degrees
@router.get("/degrees")
async def get_degrees(
    session: AsyncSession = Depends(get_session)
):
    return await service.get_degrees(session=session)

# Get a specific degree 
@router.get("/degrees/{degree_id}", response_model=DegreeRead)
async def read_degree(degree_id: str, session: AsyncSession = Depends(get_session)):
    return await service.get_degree_by_code(degree_code=degree_id, session=session)
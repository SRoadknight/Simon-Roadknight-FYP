from fastapi import APIRouter, Depends

from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user
from src.auth.models import TokenData
from src.interactions import service
from src.interactions.dependencies import verify_interaction_read_access, InteractionCommonsDep
from src.interactions.exceptions import InteractionNotFound


router = APIRouter(dependencies=[Depends(get_current_active_user)])


# Get all interactions -- this will need to have filters to be useful
@router.get("")
async def read_interactions(
    *,
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(get_current_active_staff_user),
    commons: InteractionCommonsDep 
):
    interactions = await service.get_interactions(session=session, **commons)
    return interactions


# Get a specific interaction 
@router.get("/{interaction_id}")
async def read_interaction(
    interaction_id: int,
    session: AsyncSession = Depends(get_session),
    _ = Depends(verify_interaction_read_access)
):
    interaction = await service.get_interaction_by_id(session=session, interaction_id=interaction_id)
    if interaction is None:
        raise InteractionNotFound
    return interaction


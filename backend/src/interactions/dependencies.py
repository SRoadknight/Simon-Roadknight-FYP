from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from fastapi import Depends
from src.auth.models import TokenData, UserType
from src.auth.dependencies import get_token_data
from src.interactions import service
from src.interactions.exceptions import InteractionNotFound, InteractionNotVisible
from src.interactions.models import InteractionType
from src.models import ConstrainedId
from typing import Union, Annotated



async def verify_interaction_read_access(
    interaction_id: int,
    token_data: TokenData = Depends(get_token_data),
    session: AsyncSession = Depends(get_session)
):
    interaction = await service.get_interaction_by_id(interaction_id=interaction_id, session=session)
    if interaction is None:
        raise InteractionNotFound
    if token_data.user_type in [UserType.ADMIN, UserType.STAFF]:
        return interaction
    if token_data.user_type == UserType.STUDENT:
        if interaction.student_id == token_data.related_entity_id:
            return interaction
    raise InteractionNotVisible

async def verify_interaction_modify_access(
    interaction_id: int,
    token_data: TokenData = Depends(get_token_data),
    session: AsyncSession = Depends(get_session)
):
    interaction = await service.get_interaction_by_id(interaction_id=interaction_id, session=session)
    if interaction is None:
        raise InteractionNotFound
    

    if token_data.user_type == UserType.ADMIN:
        return interaction
    elif token_data.user_type == UserType.STAFF:
        if interaction.careers_staff_id == token_data.related_entity_id:
            return interaction
    elif token_data.user_type == UserType.STUDENT:
        if interaction.student_id == token_data.related_entity_id:
            return interaction
        
    raise InteractionNotVisible

def interaction_common_params(
    student_id: Union[ConstrainedId, None] = None,
    careers_staff_id: Union[ConstrainedId, None] = None,
    type: Union[InteractionType, None] = None,
    read_staff: Union[bool, None] = False,
    read_student: Union[bool, None] = False,
    outstanding: Union[bool, None] = False
):
    return {
        "student_id": student_id,
        "careers_staff_id": careers_staff_id,
        "type": type,
        "read_staff": read_staff,
        "read_student": read_student,
        "outstanding": outstanding
    }

InteractionCommonsDep = Annotated[dict, Depends(interaction_common_params)]
from sqlmodel import select
from typing import Union
from src.groups.models import Group, GroupCreate, GroupUpdate
from src.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.groups.exceptions import GroupNameAlreadyExists

async def validate_group_name(group_data: Union[GroupCreate, GroupUpdate], session: AsyncSession = Depends(get_session)):
    if group_data.name is None:
        return group_data
    
    result = await session.exec(select(Group).where(Group.name == group_data.name))
    db_group = result.first()
    if db_group is not None:
        raise GroupNameAlreadyExists()
    return group_data
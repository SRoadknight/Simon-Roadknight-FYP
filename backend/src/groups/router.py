from fastapi import APIRouter, Depends, Path, Response, status
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user, get_current_active_student_user
from src.database import get_session
from src.groups.models import (
    GroupRead, 
    GroupCreate, 
    GroupUpdate, 
    GroupReadWithContent,
    GroupReadWithMembers
)

from src.groups import service
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.models import User
from src.auth.dependencies import get_current_active_user
from src.groups.exceptions import GroupNotFound  
from src.auth.models import TokenData
from src.groups.dependencies import validate_group_name



router = APIRouter(dependencies=[Depends(get_current_active_user)])



# Get all groups that exist in the system
@router.get("", response_model=list[GroupRead])
async def read_groups(session: AsyncSession = Depends(get_session)):
    groups = await service.get_groups(session)
    return groups
    

# Create a new group
@router.post("", response_model=GroupRead)
async def create_group(
    group_data: GroupCreate = Depends(validate_group_name), 
    session: AsyncSession = Depends(get_session), 
    current_user: User = Depends(get_current_active_staff_user),
):
    return await service.create_group(session=session, group=group_data)

# Get a specific group 
@router.get("/{group_id}", response_model=GroupRead)
async def read_group(group_id: int = Path(ge=1, le=2147483647), session: AsyncSession = Depends(get_session)):
    group = await service.get_group_by_id(session, group_id)
    if group is None:
        raise GroupNotFound()
    return group

# Update a specific group
@router.patch("/{group_id}", response_model=GroupRead)
async def update_group(
    group_id: int, 
    group_data: GroupUpdate = Depends(validate_group_name),  
    session: AsyncSession = Depends(get_session), 
    current_user: User = Depends(get_current_active_staff_user)
):
    return await service.update_group(session, group_id, group_data)

# Delete a specific group
# To delete a group all members must be disassociated from the group
# and all content must be disassociated from the group


# View all students that belong to a group
@router.get("/{group_id}/students", response_model=list[GroupReadWithMembers])
async def read_group_students(group_id: int, current_user = Depends(get_current_active_staff_user), session: AsyncSession = Depends(get_session)):
    group_students = await service.get_group_students(session, group_id)
    return group_students

# View all content that belongs to a group
@router.get("/{group_id}/content", response_model=list[GroupReadWithContent])
async def read_group_content(group_id: int, session: AsyncSession = Depends(get_session)):
    group_content = await service.get_group_content(session, group_id)
    return group_content


# Students can join a group
@router.post("/{group_id}/join")
async def join_group(
    group_id: int, 
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(get_current_active_student_user)
):
    await service.join_group(
        student_id=token_data.related_entity_id,
        group_id=group_id,
        session=session)
    
    return Response(status_code=status.HTTP_200_OK)


# Students can leave a group
@router.post("/{group_id}/leave")
async def leave_group(
    group_id: int, 
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(get_current_active_student_user)
):
    await service.leave_group(
        student_id=token_data.related_entity_id,
        group_id=group_id,
        session=session)
    return Response(status_code=status.HTTP_200_OK)
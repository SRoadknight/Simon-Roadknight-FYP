from fastapi import APIRouter, Depends, status, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user
from src.auth.models import User
from src.database import get_session
from src.content.models import ContentRead, ContentSkillTag, ContentCreate, ContentUpdate
from src.content import service


from src.content.exceptions import ContentNotFound

router = APIRouter(dependencies=[Depends(get_current_active_user)])



# Get a list of content
@router.get("", response_model=list[ContentRead])
async def read_content(session: AsyncSession = Depends(get_session)):
    return await service.get_content(session)

# View content by id
@router.get("/{content_id}", response_model=ContentRead)
async def read_content_by_id(
    content_id: int, 
    session: AsyncSession = Depends(get_session)):
    content = await service.get_content_by_id(content_id, session)
    if content is None:
        raise ContentNotFound()
    return content

# Create content
@router.post("", response_model=ContentRead)
async def create_content(
    content: ContentCreate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user)):
    return await service.create_content(content=content, session=session)

# Update content
@router.patch("/{content_id}", response_model=ContentRead)
async def update_content(
    content_id: int, 
    content: ContentUpdate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user)):
    return await service.update_content(content_id=content_id, content=content, session=session)


# Delete content
# This will require removing associated skill tags and groups first

# add a skill tag to a piece of content 
@router.post("/{content_id}/skills/{skill_id}", response_model=ContentSkillTag)
async def add_skill_tag_to_content(
    content_id: int, 
    skill_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user),
):
    await service.add_skill_tag_to_content(content_id, skill_id, session)
    return Response(status_code=status.HTTP_200_OK)

# remove a skill tag from a piece of content
@router.delete("/{content_id}/skills/{skill_id}", response_model=ContentRead)
async def remove_skill_tag_from_content(
    content_id: int, 
    skill_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user)
):
    await service.remove_skill_tag_from_content(content_id, skill_id, session)
    return Response(status_code=status.HTTP_200_OK)


# Add content to a group
@router.post("/{content_id}/groups/{group_id}", response_model=ContentRead)
async def add_content_to_group(
    content_id: int, 
    group_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user)):
    return await service.add_content_to_group(
        content_id=content_id, 
        group_id=group_id, 
        session=session)


# Remove content from a group
@router.delete("/{content_id}/groups/{group_id}")
async def remove_content_from_group(
    content_id: int, 
    group_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user)):
    await service.remove_content_from_group(
        content_id=content_id, group_id=group_id, session=session)
    return Response(status_code=status.HTTP_200_OK)

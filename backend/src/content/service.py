from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import joinedload
from src.content.models import (
    Content,
    ContentCreate,
    ContentUpdate, 
    ContentSkillTagCreate, 
    ContentSkillTag,
    ContentGroup
)
from src.content.exceptions import SkillTagAlreadyAssigned, SkillTagNotAssigned,  ContentAlreadyInGroup, ContentNotInGroup
from src.crud import create_generic, update_generic, add_skill_to_entity, remove_skill_from_entity
from src.content.exceptions import ContentNotFound
from src.groups.service import get_group_by_id
from src.groups.exceptions import GroupNotFound


# get all content in the system
async def get_content(session: AsyncSession):
    result = await session.exec(select(Content))
    content = result.all()
    return content

# get content by id
async def get_content_by_id(content_id: int, session: AsyncSession):
    result = await session.exec(
        select(Content).options(joinedload(Content.skills)).where(Content.id == content_id)
    )
    content = result.first()
    return content

# create content
async def create_content(content: ContentCreate, session: AsyncSession):
    db_content = await create_generic(
        model_class=Content,
        create_data=content,
        session=session
    )
    return db_content

# update content
async def update_content(content_id: int, content: ContentUpdate, session: AsyncSession):
    return await update_generic(
        model_id=content_id,
        update_data=content,
        model_getter=get_content_by_id,
        session=session
    )



# add a skill tag to a piece of content
async def add_skill_tag_to_content(content_id: int, skill_id: int, session: AsyncSession):
    content = await get_content_by_id(content_id, session)
    if content is None:
        raise ContentNotFound()
    await add_skill_to_entity(
        skill_tag_base_model=ContentSkillTag,
        skill_tag_create_model=ContentSkillTagCreate,
        entity_id=content_id,
        skill_id=skill_id,
        foreign_key="content_id",
        exception=SkillTagAlreadyAssigned,
        session=session
    )


# remove a skill tag from a piece of content
async def remove_skill_tag_from_content(content_id: int, skill_id: int, session: AsyncSession):
    content = await get_content_by_id(content_id, session)
    if content is None:
        raise ContentNotFound()
    await remove_skill_from_entity(
        skill_tag_base_model=ContentSkillTag,
        entity_id=content_id,
        skill_id=skill_id,
        foreign_key="content_id",
        exception=SkillTagNotAssigned,
        session=session
    )

# Check if content is already in a group
async def check_content_in_group(content_id: int, group_id: int, session: AsyncSession):
    result = await session.exec(
        select(ContentGroup).where(ContentGroup.content_id == content_id, ContentGroup.group_id == group_id)
    )
    content_group = result.first()
    return content_group

# Add content to a group
async def add_content_to_group(content_id: int, group_id: int, session: AsyncSession):
    content = await get_content_by_id(content_id, session)
    if content is None:
        raise ContentNotFound()
    content_copy = content.model_copy()
    group = await get_group_by_id(group_id=group_id, session=session)
    if group is None:
        raise GroupNotFound()
    if await check_content_in_group(content_id, group_id, session):
        raise ContentAlreadyInGroup()
    content_group_data = {"content_id": content_id, "group_id": group_id}
    db_content_group = ContentGroup.model_validate(content_group_data)
    session.add(db_content_group)
    await session.commit()
    await session.refresh(db_content_group)
    return content_copy

# Remove content from a group
async def remove_content_from_group(content_id: int, group_id: int, session: AsyncSession):
    content = await get_content_by_id(content_id, session)
    if content is None:
        raise ContentNotFound()
    group = await get_group_by_id(group_id=group_id, session=session)
    if group is None:
        raise GroupNotFound()
    content_group = await check_content_in_group(content_id, group_id, session)
    if content_group is None:
        raise ContentNotInGroup()
    await session.delete(content_group)
    await session.commit()
    
    



    
from src.skill_tags.exceptions import SkillTagAlreadyExists, SkillTagNameEmpty, SkillTagInactive, SkillTagNotFound
from src.skill_tags.models import SkillTag, SkillTagCreate, SkillTagUpdate
from src.skill_tags import service
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from fastapi import Depends
from typing import Union


async def valid_skill_tag_create(
        skill_tags: Union[SkillTagCreate, list[SkillTagCreate]], 
        session: AsyncSession = Depends(get_session)
        ):
    if isinstance(skill_tags, list):
        # If a list is provided, iterate over it
        
        # Check that the same name is not provided twice in skill_tags
        skill_names = [skill.name for skill in skill_tags]
        if len(skill_names) != len(set(skill_names)):
            raise SkillTagAlreadyExists(detail="Duplicate skill names provided.")

        already_exists = []
        for skill in skill_tags:
            if skill.name == "":
                raise SkillTagNameEmpty()
            if await service.get_skill_by_name(skill.name, session=session):
               already_exists.append(skill.name)
        if already_exists:
            # create a string to respond containing all the skills that already exist
            already_exists = ", ".join(already_exists)
            raise SkillTagAlreadyExists(
                detail=f"Skills already exist: {already_exists}. No skills were created."
                )
        return skill_tags
            
    else:
        # Single SkillTagCreate instance
        if skill_tags.name == "":
            raise SkillTagNameEmpty()
        if await service.get_skill_by_name(skill_tags.name, session=session):
            raise SkillTagAlreadyExists()
        return skill_tags
    
async def valid_skill_tag_update(
        skill_tag: SkillTagUpdate, 
        session: AsyncSession = Depends(get_session)
        ):
    # check if the skill tag name is being updated 
    if skill_tag.name == "":
        raise SkillTagNameEmpty()
    elif await service.get_skill_by_name(skill_tag.name, session=session):
        raise SkillTagAlreadyExists()
    
    return skill_tag

async def skill_tag_exists(skill_id: int, session: AsyncSession = Depends(get_session)):
    skill_tag = await service.get_skill_by_id(skill_id, session=session)
    if not skill_tag:
        raise SkillTagNotFound()
    return skill_tag


async def valid_active_skill_tag(skill_tag: SkillTag = Depends(skill_tag_exists)):
    if not skill_tag.active:
        raise SkillTagInactive()
    return skill_tag

       
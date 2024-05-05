from datetime import datetime
from typing import Union, Type, Any, Callable, Dict
from sqlmodel import SQLModel, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.skill_tags.service import get_skill_by_id, get_skill_by_name, create_skill_tag
from src.exceptions import DetailedHTTPException, NotFound
from src.skill_tags.exceptions import SkillTagNotFound, SkillNameAndSkillIdBothProvided, SkillNameAndSkillIdNotProvided


async def create_generic(
        model_class: Type[SQLModel] , 
        create_data: SQLModel, 
        session: AsyncSession,
        extra_data: Union[Dict[str, Any], None] = None,
        commit: bool = True):
    if extra_data:
        db_model = model_class.model_validate(create_data, update=extra_data)
    else:
        db_model = model_class.model_validate(create_data)
    if commit:
        session.add(db_model)
        await session.commit()
        await session.refresh(db_model)
    return db_model


    
async def update_generic(
        model_id: Any, 
        update_data: SQLModel, 
        model_getter: Callable, 
        session: AsyncSession
        ):
    db_model = await model_getter(model_id, session)
    if db_model is None:
        raise NotFound()
    model_data = update_data.model_dump(exclude_unset=True)
    db_model = db_model.sqlmodel_update(model_data)
    session.add(db_model)
    return db_model


# SQLModel get entity by id or constrained type where the entity is the type of SQLModel
def get_entity_by_id(session: Session, entity: Type[SQLModel], entity_id: Any) -> Union[SQLModel, None]:
    entity = session.get(entity, entity_id)
    return entity


# Skills CRUD

# check skill in entity
async def check_skill_in_entity(
        *,
        entity_id: int,
        skill_name: Union[str, None] = None,
        skill_id: Union[int, None] = None,
        skill_tag_base_model: Type[SQLModel],
        foreign_key: str,
        session: AsyncSession):
    
    # Check if skill name exists in skill tag table
    if skill_name:
        skill_tag = await get_skill_by_name(skill_name, session=session)
        if not skill_tag:
            return None
    else:
        skill_tag = await get_skill_by_id(skill_id, session=session)
        if not skill_tag:
            return None
    
    entity_column = getattr(skill_tag_base_model, foreign_key)
    result = await session.exec(
        select(skill_tag_base_model).where(
            entity_column == entity_id,
            skill_tag_base_model.skill_id == skill_tag.id
        )
    )
    return result.first()


# add skill to existing entity which may already have skills 
async def add_skill_to_entity(
        *,
        skill_tag_base_model: Type[SQLModel],
        entity_id: int,
        skill_name: Union[str, None] = None,
        skill_id: Union[int, None] = None,
        foreign_key: str,
        session: AsyncSession,
        commit: bool = True,
        **kwargs: Dict[str, Any]):
    
    if skill_name is None and skill_id is None:
        raise SkillNameAndSkillIdNotProvided()
    if skill_name and skill_id:
        raise SkillNameAndSkillIdBothProvided()

    
    if skill_name:
        skill_tag = await get_skill_by_name(skill_name, session=session)
        if not skill_tag:
            skill_tag = await create_skill_tag({"name": skill_name}, session=session)
        else:
            if await check_skill_in_entity(
                    entity_id=entity_id,
                    skill_name=skill_name,
                    skill_tag_base_model=skill_tag_base_model,
                    foreign_key=foreign_key,
                    session=session):
                return None
    else:
        skill_tag = await get_skill_by_id(skill_id, session=session)
        if not skill_tag:
            raise SkillTagNotFound(detail="Skill tag not found")
        if await check_skill_in_entity(
                entity_id=entity_id,
                skill_id=skill_id,
                skill_tag_base_model=skill_tag_base_model,
                foreign_key=foreign_key,
                session=session):
            return None
   
    skill_tag_data = {foreign_key: entity_id, "skill_id": skill_tag.id, **kwargs}
    db_skill_tag = skill_tag_base_model.model_validate(skill_tag_data)
    session.add(db_skill_tag)
    skill_tag.last_used = datetime.now()
    await session.commit()
    await session.refresh(db_skill_tag)
    return db_skill_tag

# remove skill generic
async def remove_skill_from_entity(
        entity_id: int,
        skill_id: int,
        skill_tag_base_model: Type[SQLModel],
        foreign_key: str,
        exception: Type[DetailedHTTPException],
        session: AsyncSession):
    db_skill_tag = await check_skill_in_entity(
        entity_id=entity_id,
        skill_id=skill_id,
        skill_tag_base_model=skill_tag_base_model,
        foreign_key=foreign_key,
        session=session)
    if not db_skill_tag:
        raise exception
    await session.delete(db_skill_tag)
    await session.commit()
    

# add skils straight after creating an entity
async def add_skills_to_entity_on_create(
        entity_model: Type[SQLModel],
        entity_id: int,
        skill_data: list[Dict[str, Any]],
        foreign_key: str,
        session: AsyncSession):
    # if skill data isn't present or is an empty dict return None
    if not skill_data:
        return None
    
    # Valid skills either have a skill_id or a skill_name
    valid_skill_data_entries = [
        skill_entry for skill_entry in skill_data if 'skill_id' in skill_entry or 'skill_name' in skill_entry]
    unique_skills = {}
    for skill_entry in valid_skill_data_entries: 
        key = (skill_entry.get("skill_id"), skill_entry.get("skill_name"))
        if key not in unique_skills:
            unique_skills[key] = skill_entry
    for skill_entry in unique_skills.values():
        await add_skill_to_entity(
            skill_tag_base_model=entity_model,
            entity_id=entity_id,
            skill_name=skill_entry.get("skill_name"),
            skill_id=skill_entry.get("skill_id"),
            foreign_key=foreign_key,
            session=session
        )
    return None

async def validate_skill_tags(skill_data: list[Dict[str, Any]], session: AsyncSession):
    # skill data 
    if skill_data:
        # get all skill tags "skill_id" and see if they exist
        skill_ids = [skill_entry for skill_entry in skill_data if 'skill_id' in skill_entry]
        not_found_skill_ids = []
        unique_skills = {
        skill_entry['skill_id']: skill_entry for skill_entry in skill_ids}.values()
        for skill_dict in unique_skills:
            skill_id = skill_dict['skill_id']
            skill = await get_skill_by_id(skill_id, session=session)
            if not skill:
                not_found_skill_ids.append(skill_id)
        if not_found_skill_ids:
            raise SkillTagNotFound(detail=f"Skill tags not found for ids: {not_found_skill_ids}")
    return None
    
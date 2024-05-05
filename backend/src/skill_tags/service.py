from sqlmodel import  select
from src.skill_tags.models import SkillTag, SkillTagCreate
from src.skill_tags.exceptions import SkillTagNotFound
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_skills(session: AsyncSession):
    result = await session.exec(select(SkillTag))
    skill_tags = result.all()
    return skill_tags

async def get_skill_by_name(skill_name: str, session: AsyncSession):
    result = await session.exec(select(SkillTag).where(SkillTag.name == skill_name))
    skill_tag = result.first()
    return skill_tag

async def get_skill_by_id(skill_id: int, session: AsyncSession):
    result = await session.exec(select(SkillTag).where(SkillTag.id == skill_id))
    skill_tag =  result.first()

    if skill_tag is None:
        raise SkillTagNotFound(detail=f"Skill tag not found for id: {skill_id}")
    
    return skill_tag

async def create_skill_tag(skill_tag: SkillTagCreate, session: AsyncSession):
    db_skill_tag = SkillTag.model_validate(skill_tag)
    session.add(db_skill_tag)
    await session.commit()
    await session.refresh(db_skill_tag)
    return db_skill_tag



async def validate_skill_tags(skill_tag_ids: list[int], session: AsyncSession):
    result = await session.exec(select(SkillTag).where(SkillTag.id.in_(skill_tag_ids)))
    skill_tags = result.all()
    if len(skill_tags) != len(skill_tag_ids):
        raise SkillTagNotFound(detail="One or more skill tags not found")
    return skill_tags


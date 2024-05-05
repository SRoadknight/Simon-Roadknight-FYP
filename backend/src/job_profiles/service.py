from sqlmodel import select
from sqlalchemy.orm import joinedload
from src.job_profiles.models import JobProfile, JobProfileCreate, JobProfileUpdate, JobProfileSkillTag, JobProfileSkillTagCreate
from src.job_profiles.exceptions import JobProfileNotFound, SkillTagAlreadyAssigned, SkillNotAssignedToJobProfile
from sqlmodel.ext.asyncio.session import AsyncSession
from src.crud import add_skill_to_entity, remove_skill_from_entity, create_generic, add_skills_to_entity_on_create, update_generic
from typing import Any, Dict

async def get_job_profiles(session: AsyncSession):
    result = await session.exec(select(JobProfile))
    job_profiles = result.all()
    return job_profiles


async def get_job_profile_by_id(job_profile_id: int, session: AsyncSession):
    result = await session.exec(
        select(JobProfile).options(joinedload(JobProfile.skills)).where(JobProfile.id == job_profile_id))
    job_profile = result.first()
    if not job_profile:
        raise JobProfileNotFound()
    
    return job_profile

async def get_job_profile_by_title(job_profile_title: str, session: AsyncSession):
    result = await session.exec(select(JobProfile).where(JobProfile.title == job_profile_title))
    job_profile = result.first()
    return job_profile


async def soft_delete_job_profile(job_profile_id: int, session: AsyncSession):
    job_profile = await get_job_profile_by_id(job_profile_id, session)
    job_profile.is_active = False
    session.add(job_profile)
    await session.commit()
    await session.refresh(job_profile)
    return job_profile

async def get_job_profile_skill(job_profile_id: int, skill_id: int, session: AsyncSession):
    job_profile = await get_job_profile_by_id(job_profile_id, session)
    job_profile_skill = await session.exec(
        select(JobProfileSkillTag).options(joinedload(JobProfileSkillTag.skill)).where(
            JobProfileSkillTag.job_profile_id == job_profile_id,
            JobProfileSkillTag.skill_tag_id == skill_id
        )
    )
    return job_profile_skill.first() 

async def get_job_profile_skills(job_profile_id: int, session: AsyncSession):
    await get_job_profile_by_id(job_profile_id, session)
    job_profile_skills = await session.exec(
        select(JobProfileSkillTag).options(joinedload(JobProfileSkillTag.skill)).where(
            JobProfileSkillTag.job_profile_id == job_profile_id
        )
    )
    return job_profile_skills.all()



async def add_skill_to_job_profile(
    job_profile_id: int, 
    skill_id: int, 
    job_profile_skill_tag: JobProfileSkillTagCreate,
    session: AsyncSession
    ):
    await add_skill_to_entity(
    skill_tag_base_model=JobProfileSkillTag,
    skill_tag_create_model=JobProfileSkillTagCreate,
    entity_id=job_profile_id,
    skill_id=skill_id,
    foreign_key="job_profile_id",
    exception=SkillTagAlreadyAssigned,
    session=session,
    weight=job_profile_skill_tag.weight
)
    
    return await get_job_profile_by_id(job_profile_id, session=session)


async def remove_skill_from_job_profile(
    job_profile_id: int, 
    skill_id: int, 
    session: AsyncSession
    ):
    await remove_skill_from_entity(
        skill_tag_base_model=JobProfileSkillTag,
        entity_id=job_profile_id,
        skill_id=skill_id,
        foreign_key="job_profile_id",
        exception=SkillNotAssignedToJobProfile,
        session=session
    )
    return await get_job_profile_by_id(job_profile_id, session=session)

async def add_job_profile_skills(
        job_profile_id: int,
          skill_data: list[Dict[str, Any]], 
          session: AsyncSession):
    await add_skills_to_entity_on_create(
        entity_id=job_profile_id, 
        entity_model=JobProfileSkillTag, 
        skill_data=skill_data, 
        foreign_key="job_profile_id",
        session=session
    )
    return await get_job_profile_by_id(job_profile_id, session=session)

async def create_job_profile(job_profile: JobProfileCreate, session: AsyncSession):
    db_job_profile = await create_generic(
        model_class=JobProfile,
        create_data=job_profile,
        session=session
        )
    await add_job_profile_skills(
        job_profile_id=db_job_profile.id,
        skill_data=job_profile.skill_data,
        session=session
    )
    await session.commit()
    await session.refresh(db_job_profile)
    return db_job_profile

async def update_job_profile(job_profile_id: int, job_profile: JobProfileUpdate, session: AsyncSession):
    return await update_generic(
        model_id=job_profile_id,
        update_data=job_profile,
        model_getter=get_job_profile_by_id,
        session=session
        )
    

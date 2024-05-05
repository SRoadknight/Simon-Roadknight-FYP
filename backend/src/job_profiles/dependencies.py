from src.job_profiles.exceptions import JobProfileAlreadyExists
from src.job_profiles.models import JobProfileCreate, JobProfileUpdate
from src.job_profiles import service
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from fastapi import Depends

async def validate_job_profile_create(
        job_profile: JobProfileCreate, 
        session: AsyncSession = Depends(get_session)
        ):
    if await service.get_job_profile_by_title(job_profile.title, session=session):
        raise JobProfileAlreadyExists()
    return job_profile

async def validate_job_profile_update(
        job_profile: JobProfileUpdate, 
        session: AsyncSession = Depends(get_session)
        ):
    if await service.get_job_profile_by_title(job_profile.title, session=session):
        raise JobProfileAlreadyExists()
    return job_profile

async def get_job_profile_by_id(job_profile_id: int, session: AsyncSession = Depends(get_session)):
    job_profile = await service.get_job_profile_by_id(job_profile_id, session=session)
    return job_profile
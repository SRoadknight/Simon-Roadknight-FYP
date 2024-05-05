from fastapi import APIRouter, Depends

from src.auth.models import User
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user
from src.job_profiles.models import (
    JobProfile, 
    JobProfileCreate, 
    JobProfileRead, 
    JobProfileUpdate,
    JobProfileSkillTagCreate,
    JobProfileSkillTagRead
)
from src.job_profiles import service
from src.job_profiles.dependencies import (
    validate_job_profile_create, 
    validate_job_profile_update,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session

from src.skill_tags.dependencies import valid_active_skill_tag, skill_tag_exists
from src.job_profiles.dependencies import get_job_profile_by_id
from src.skill_tags.models import SkillTag



router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Get all job profiles
@router.get("", response_model=list[JobProfileRead])
async def read_job_profiles(session: AsyncSession = Depends(get_session)):
    return await service.get_job_profiles(session=session)

# Get a single job profile
@router.get("/{job_profile_id}", response_model=JobProfileRead)
async def read_job_profile(
    job_profile_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    job_profile = await service.get_job_profile_by_id(job_profile_id, session=session)
    
    return job_profile


# Create a new job profile
@router.post("", response_model=JobProfileRead)
async def create_job_profile(
    job_profile: JobProfileCreate = Depends(validate_job_profile_create),
    user: User = Depends(get_current_active_staff_user),
    session: AsyncSession = Depends(get_session)
    ):
    return await service.create_job_profile(job_profile, session=session)


# Update a job profile
@router.patch("/{job_profile_id}", response_model=JobProfileRead)
async def update_job_profile(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    job_profile_id: int,
    job_profile: JobProfileUpdate = Depends(validate_job_profile_update),
    session: AsyncSession = Depends(get_session)
    ):
    return await service.update_job_profile(job_profile_id, job_profile, session=session)
    

# Delete a job profile (soft delete making it inactive) 
@router.patch("/{job_profile_id}/soft-delete", response_model=JobProfileRead)
async def delete_job_profile(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    job_profile_id: int,
    session: AsyncSession = Depends(get_session)
    ):
   
    return await service.soft_delete_job_profile(job_profile_id, session=session)

# Get all skills for a job profile
@router.get("/{job_profile_id}/skills", response_model=list[JobProfileSkillTagRead])
async def read_job_profile_skills(
    job_profile_id: int,
    session: AsyncSession = Depends(get_session),
    job_profile_checker: JobProfile = Depends(get_job_profile_by_id)
    ):
    return await service.get_job_profile_skills(job_profile_id, session=session)


# Add a skill to a job profile
@router.post("/{job_profile_id}/add-skill/{skill_id}", response_model=JobProfileRead)
async def add_skill_to_job_profile(
    job_profile_id: int, 
    skill_id: int, 
    job_profile_skill_tag: JobProfileSkillTagCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user),
    skill_tag_checker: SkillTag = Depends(valid_active_skill_tag)):
    return await service.add_skill_to_job_profile(
        job_profile_id,
        skill_id,
        job_profile_skill_tag, 
        session=session
    )

# Remove a skill from a job profile
@router.delete("/{job_profile_id}/remove-skill/{skill_id}", response_model=JobProfileRead)
async def remove_skill_from_job_profile(
    job_profile_id: int, 
    skill_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user),
    job_profile_checker: JobProfile = Depends(get_job_profile_by_id),
    skill_tag_checker: SkillTag = Depends(skill_tag_exists)):
    return await service.remove_skill_from_job_profile(
        job_profile_id,
        skill_id,
        session=session
    )
from fastapi import APIRouter, Depends, Response, status
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user
from src.database import get_session
from src.job_posts import service
from src.job_posts.models import JobPostRead
from sqlmodel.ext.asyncio.session import AsyncSession
from src.job_posts.models import JobPost, JobPostCreate, JobPostUpdate
from src.job_posts.dependencies import (
    verify_job_post_read_access, 
    verify_job_post_access, 
    verify_staff_or_company,
    valid_skill_addition_for_uni_job_post,
    valid_skill_removal_for_uni_job_post,
)
from src.auth.dependencies import get_token_data
from src.applications.models import JobApplicationCreate, JobApplicationReadWithStudent
from src.auth.models import User
from src.job_posts.models import JobSource

router = APIRouter(dependencies=[Depends(get_current_active_user)])


# Get all job posts that are ongoing and visible to students
@router.get("", response_model=list[JobPostRead])
async def read_job_posts(session: AsyncSession = Depends(get_session)):
    return await service.get_job_posts(session=session)

# Get a job post by id
@router.get("/{job_post_id}")
async def read_job_post(
    *,
    job_post: JobPost = Depends(verify_job_post_read_access),
    ):
    return job_post

# Create a new job post
@router.post("")
async def create_job_post(
    *,
    session: AsyncSession = Depends(get_session),
    job_post: JobPostCreate,
    current_user = Depends(get_current_active_staff_user),
    token_data = Depends(get_token_data)
    ):
    job_post = await service.create_job_post_full(
        session=session, 
        job_post=job_post, 
        entity_id=token_data.user_id,
        job_source=JobSource.STAFF)
    return job_post

# Update a job post
@router.patch("/{job_post_id}", response_model=JobPostRead)
async def update_job_post(
    *,
    user: User = Depends(verify_staff_or_company),
    job_post: JobPost = Depends(verify_job_post_access),
    job_post_update: JobPostUpdate,
    session: AsyncSession = Depends(get_session)
    ):
    db_job_post = await service.update_job_post(
        session=session, 
        job_post=job_post, 
        update_data=job_post_update)
    return db_job_post


# Delete a job post (soft-delete)
@router.patch("/{job_post_id}/soft-delete")
async def delete_job_post(
    *,
    user: User = Depends(verify_staff_or_company),
    job_post: JobPost = Depends(verify_job_post_access),
    session: AsyncSession = Depends(get_session)
    ):
    await service.delete_job_post(session=session, job_post=job_post)
    return Response(status_code=status.HTTP_200_OK)


# Student saves/likes a job post
@router.post("/{job_post_id}/save")
async def save_job_post(
    *,
    job_post: JobPost = Depends(verify_job_post_read_access),
    session: AsyncSession = Depends(get_session),
    token_data = Depends(get_token_data)
    ):
    await service.save_job_post(
        session=session, 
        job_post_id=job_post.id, 
        student_id=token_data.related_entity_id)
    return Response(status_code=status.HTTP_200_OK)


# Student un-saves/un-likes a job post
@router.delete("/{job_post_id}/save")
async def unsave_job_post(
    *,
    job_post: JobPost = Depends(verify_job_post_read_access),
    session: AsyncSession = Depends(get_session),
    token_data = Depends(get_token_data)
    ):
    await service.unsave_job_post(
        session=session, 
        job_post_id=job_post.id, 
        student_id=token_data.related_entity_id)
    return Response(status_code=status.HTTP_200_OK
)



# add an application to a job post
@router.post("/{job_post_id}/applications")
async def add_application_to_job_post(
    *,
    job_post: JobPost = Depends(verify_job_post_read_access),
    job_application: JobApplicationCreate,
    session: AsyncSession = Depends(get_session),
    token_data = Depends(get_token_data)
    ):
    db_application = await service.add_application_to_job_post(
        session=session, 
        job_post_id=job_post.id, 
        job_application=job_application,
        student_id=token_data.related_entity_id)
    return db_application


# Get all applications for a job post
@router.get("/{job_post_id}/applications", response_model=list[JobApplicationReadWithStudent])
async def read_job_post_applications(
    *,
    job_post: JobPost = Depends(verify_job_post_access),
    session: AsyncSession = Depends(get_session)
    ):
    return await service.get_job_post_applications(session=session, job_post_id=job_post.id)


# Students and staff can add skills to a job post (where source is not student or company) through this endpoint
# Students and companies will have their own endpoint for their own job posts
@router.post("/{job_post_id}/add-skill/{skill_id}")
async def add_job_post_skill(
    *,
    job_post: JobPost = Depends(valid_skill_addition_for_uni_job_post),
    session: AsyncSession = Depends(get_session),
    skill_id: int
    ):
    await service.add_job_post_skill(
        session=session,
        job_post_id=job_post.id, 
        skill_id=skill_id)
    return Response(status_code=status.HTTP_200_OK)

# remove a skill from a job post
@router.delete("/{job_post_id}/remove-skill/{skill_id}")
async def remove_job_post_skill(
    *,
    job_post: JobPost = Depends(valid_skill_removal_for_uni_job_post),
    session: AsyncSession = Depends(get_session),
    skill_id: int
    ):
    await service.remove_job_post_skill(
        session=session,
        job_post_id=job_post.id, 
        skill_id=skill_id)
    return Response(status_code=status.HTTP_200_OK)


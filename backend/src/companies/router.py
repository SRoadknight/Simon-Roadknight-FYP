from fastapi import APIRouter, Depends, Response, status, Query
from src.auth.dependencies import (
    get_current_active_user, 
    get_current_active_staff_user,
    get_current_active_company_user
)
from src.companies.models import (
    CompanyRead, 
    CompanyUserCreate,
    CompanyUpdate
)
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from src.companies import service
from src.companies.dependencies import validate_company_user_create, valid_company_update
from src.auth.models import TokenData, User
from src.companies.exceptions import CompanyNotFound
from src.models import ConstrainedId
from src.job_posts.models import JobPost, JobPostUpdate, JobPostCreate
from src.job_posts.dependencies import verify_job_post_access
from src.applications.models import JobApplicationStage
from typing import Union


router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Get all companies
@router.get("", response_model=list[CompanyRead])
async def read_companies(session: AsyncSession = Depends(get_session)):
    return await service.get_companies(session=session)


# create a company
@router.post("", response_model=CompanyRead)
async def create_company(
    *,
    session: AsyncSession = Depends(get_session),
    company_user: CompanyUserCreate = Depends(validate_company_user_create),
    current_user: CompanyUserCreate = Depends(get_current_active_staff_user),
):
    return await service.create_company(session=session, company_user=company_user)

# company gets their own profile 
@router.get("/me", response_model=CompanyRead)
async def get_own_company_profile(
    token_data: TokenData = Depends(get_current_active_company_user),
    session: AsyncSession = Depends(get_session),
):
    company = await service.get_company_by_id(session=session, company_id=token_data.related_entity_id)
    if company is None:
        raise CompanyNotFound()
    return company
    
# company updates their own profile
@router.patch("/me", response_model=CompanyRead)
async def update_own_company_profile(
    *,
    token_data: TokenData = Depends(get_current_active_company_user),
    company_update: CompanyUpdate = Depends(valid_company_update),
    session: AsyncSession = Depends(get_session)
):
    company =  service.update_company(
        session=session, 
        company=company_update,
        comapny_id=token_data.related_entity_id)
    return company

# get all student applications for a company
@router.get("/me/applications")
async def get_company_applications(
    token_data: TokenData = Depends(get_current_active_company_user),
    session: AsyncSession = Depends(get_session),
    stages: Union[list[JobApplicationStage], None] = Query(None)
):
    job_applications = await service.get_company_job_applications(
        session=session, 
        company_id=token_data.related_entity_id,
        stages = stages)
    return job_applications
    
# get all job posts for a company
@router.get("/me/job-posts")
async def get_company_job_posts(
    token_data: TokenData = Depends(get_current_active_company_user),
    session: AsyncSession = Depends(get_session),
):
    job_posts = await service.get_company_job_posts(
        session=session, 
        company_id=token_data.related_entity_id)
    return job_posts


# get a company by id
@router.get("/{company_id}", response_model=CompanyRead)
async def get_company_by_id(
    company_id: ConstrainedId,
    session: AsyncSession = Depends(get_session),
):
    company = await service.get_company_by_id(session=session, company_id=company_id)
    if company is None:
        raise CompanyNotFound()
    return company

# staff member can update a company
@router.patch("/{company_id}", response_model=CompanyRead)
async def update_company(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    company_id: ConstrainedId,
    company_update: CompanyUpdate = Depends(valid_company_update),
    session: AsyncSession = Depends(get_session),
):
    company = await service.update_company(
        session=session, 
        company_update=company_update, 
        company_id=company_id)
    return company

# staff can view students applications for a company 
@router.get("/{company_id}/job-applications")
async def get_company_applications(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    company_id: ConstrainedId,
    session: AsyncSession = Depends(get_session),
    stages: Union[list[JobApplicationStage], None] = Query(None)
):
    job_applications = await service.get_company_job_applications(
        session=session, 
        company_id=company_id,
        stages = stages)
    return job_applications

# students and staff can get a list of job posts for a company
@router.get("/{company_id}/job-posts",)
async def get_company_job_posts(
    *,
    company_id: ConstrainedId,
    session: AsyncSession = Depends(get_session),
):
    job_posts = await service.get_company_job_posts(
        session=session, 
        company_id=company_id)
    return job_posts

# company creates a job post
@router.post("/job-posts")
async def create_company_job_post(
    *,
    token_data: TokenData = Depends(get_current_active_company_user),
    job_post: JobPostCreate,
    session: AsyncSession = Depends(get_session),
):
    job_post = await service.create_company_job_post(
        session=session,
        job_post=job_post,
        entity_id=token_data.related_entity_id)
    return job_post

# company updates a job post
@router.patch("/job-posts/{job_post_id}")
async def update_company_job_post(
    *,
    token_data: TokenData = Depends(get_current_active_company_user),
    job_post: JobPost = Depends(verify_job_post_access),
    job_post_id: int,
    job_post_update: JobPostUpdate,
    session: AsyncSession = Depends(get_session),
):
    await service.update_company_job_post(
        session=session, 
        job_post=job_post, 
        update_data=job_post_update)
    return Response(status_code=status.HTTP_200_OK)

# add a skill tag to a company job post 
@router.post("/{company_id}/job-posts/{job_post_id}/skills")
async def add_job_post_skills(
    *,
    token_data: TokenData = Depends(get_current_active_company_user),
    job_post: JobPost = Depends(verify_job_post_access),
    job_post_id:  int,
    skill_id: int, 
    session: AsyncSession = Depends(get_session),
):
    await service.add_job_post_skill(
        session=session, 
        job_post_id=job_post_id, 
        skill_id=skill_id)
    return Response(status_code=status.HTTP_201_CREATED)


# remove a skill tag from a company job post
@router.delete("/{company_id}/job-posts/{job_post_id}/skills/{skill_id}")
async def remove_job_post_skills(
    *,
    token_data: TokenData = Depends(get_current_active_company_user),
    job_post: JobPost = Depends(verify_job_post_access),
    job_post_id:  int,
    skill_id: int, 
    session: AsyncSession = Depends(get_session),
):
    await service.remove_job_post_skills(
        session=session, 
        job_post_id=job_post_id, 
        skill_id=skill_id)
    return Response(status_code=status.HTTP_200_OK)


from datetime import datetime
from typing import Union
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import joinedload
from src.companies.models import Company, CompanyUserCreate, CompanyUpdate, CompanyJobPost
from src.companies.exceptions import CompanyNotFound, CompanyAlreadyRegistered
from src.auth.service import disable_user_account, get_user_by_id, create_user
from src.crud import update_generic
from src.applications.models import JobApplication, JobApplicationStage
from src.job_posts.models import JobPost, JobPostUpdate, JobPostCreate, JobSource
from src.job_posts.service import (
    get_job_post_by_id,
    create_job_post_full, 
    update_job_post,
    add_job_post_skill, 
    remove_job_post_skill
)
from src.job_posts.exceptions import JobPostNotFound
from src.models import ConstrainedId
from sqlalchemy import or_
from src.auth.models import User
from pydantic import EmailStr


# get all companies
async def get_companies(session: AsyncSession):
    result = await session.exec(select(Company))
    companies = result.all()
    return companies


# get company by id 
async def get_company_by_id(company_id: ConstrainedId, session: AsyncSession):
    result = await session.exec(select(Company).where(Company.id == company_id))
    company = result.first()
    return company

# get company by name
async def get_company_by_name(session: AsyncSession, company_name: str):
    result = await session.exec(select(Company).where(Company.name == company_name))
    company = result.first()
    return company

async def check_company_exists(
        session: AsyncSession, 
        company_id: Union[ConstrainedId, None] = None, 
        company_name: Union[str, None] = None, 
        user_email: Union[EmailStr, None] = None):
    
    conditions = []

    if company_id:
        conditions.append(Company.id == company_id)

    if company_name:
        conditions.append(Company.name == company_name)

    query = select(Company).options(joinedload(Company.user))
    if conditions:
        query = query.where(or_(*conditions))

    result = await session.exec(query)
    existing_company = result.first()

    if existing_company:
        if company_id is not None and existing_company.id == company_id:
            raise CompanyAlreadyRegistered(detail="Company already registered with that id")
        if company_name is not None and existing_company.name == company_name:
            raise CompanyAlreadyRegistered(detail="Company already registered with that name")
    
    if user_email:
        result = await session.exec(select(User).where(User.email_address == user_email))
        existing_user = result.first()
        if existing_user:
            raise CompanyAlreadyRegistered(detail="Company already registered with that email")

 

# create a company
async def create_company(session: AsyncSession, company_user: CompanyUserCreate):
    # create the user account
    db_company_user = await create_user(session=session, user=company_user)
    # create the company
    # convert AnyHttpUrl to str
    company_extra_data = {"user_id": db_company_user.id}
    db_company = Company.model_validate(company_user,  update=company_extra_data)
    session.add(db_company)
    await session.commit()
    await session.refresh(db_company)
    return db_company

# disable a company
async def disable_company(session: AsyncSession, company: Company):
    # disable the user account
    db_user = await get_user_by_id(session=session, user_id=company.user_id)
    return await disable_user_account(session=session, user=db_user)

# update a company
async def update_company(
        session: AsyncSession,
        company_update: CompanyUpdate,
        company_id: int):
    return await update_generic(
        model_id=company_id,
        update_data=company_update,
        model_getter=get_company_by_id,
        session=session
    )

# get company job applications 
async def get_company_job_applications(session: AsyncSession, company_id: int, stages: Union[list[JobApplicationStage], None] = None):
    # get the company
    company = await get_company_by_id(session=session, company_id=company_id)
    if not company:
        raise CompanyNotFound()
    # get all the applications for the company 
    query = (select(JobApplication)
             .join(JobPost, JobApplication.job_post_id == JobPost.id)
             .join(CompanyJobPost, JobPost.id == CompanyJobPost.job_post_id)
             .where(CompanyJobPost.company_id == company_id))
    if stages:
        query = query.where(JobApplication.stage.in_(stages))
    result = await session.exec(query)
    job_applications = result.all()
    return job_applications

# get company job post 
async def get_company_job_post(
        session: AsyncSession,
        company_id: ConstrainedId,
        job_post_id: int):
    # get the company to make sure it exists
    company = await get_company_by_id(session=session, company_id=company_id)
    if company is None:
        raise CompanyNotFound()
    # get the job post
    result = await session.exec(
        select(CompanyJobPost).where(
            (CompanyJobPost.company_id == company_id) &
            (CompanyJobPost.job_post_id == job_post_id)
        ))
    company_job_post = result.first()
    return company_job_post


# get company job posts
async def get_company_job_posts(session: AsyncSession, company_id: ConstrainedId):
    # get the company
    company = await get_company_by_id(session=session, company_id=company_id)
    if company is None:
        raise CompanyNotFound()
    # get all the job posts for the company
    result = await session.exec(
        select(JobPost)
        .join(CompanyJobPost, JobPost.id == CompanyJobPost.job_post_id)
        .where(CompanyJobPost.company_id == company_id)
    )
    job_posts = result.all()
    return job_posts

# create company job post
async def create_company_job_post(
        session: AsyncSession,
        job_post: JobPostCreate,
        entity_id: int,
):
    db_job_post = await create_job_post_full(
        session=session,
        job_post=job_post,
        entity_id=entity_id,
        job_source=JobSource.COMPANY
    )
    return db_job_post

# update company job post
async def update_company_job_post(
        session: AsyncSession,
        job_post: JobPost,
        job_post_update: JobPostUpdate):
    
    db_job_post = await update_job_post(
        session=session, 
        job_post=job_post, 
        update_data=job_post_update
    )
    return db_job_post

# add a skill tag to a company job post
async def add_skill_tag_to_company_job_post(
    session: AsyncSession,
    job_post_id: int,
    skill_id: int
):
    job_post = await get_job_post_by_id(session=session, job_post_id=job_post_id)
    if job_post is None:
        raise JobPostNotFound()
    
    await add_job_post_skill(
        session=session,
        job_post_id=job_post_id,
        skill_id=skill_id
    )

# remove a skill tag from a company job post
async def remove_skill_tag_from_company_job_post(
    session: AsyncSession,
    job_post_id: int,
    skill_id: int
):
    job_post = await get_job_post_by_id(session=session, job_post_id=job_post_id)
    if job_post is None:
        raise JobPostNotFound()
    
    await remove_job_post_skill(
        session=session,
        job_post_id=job_post_id,
        skill_id=skill_id
    )
    
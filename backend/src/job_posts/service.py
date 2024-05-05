from datetime import datetime
from typing import Type, Any, Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select
from sqlalchemy.orm import selectinload
from src.job_posts.models import (
    JobPost, 
    Visibility, 
    JobPostCreate, 
    JobSource, 
    JobPostSkillTag,
    JobPostUpdate,
    JobPostStatus,
    SavedJobPost
)
from src.students.models import StudentJobPost
from src.companies.models import CompanyJobPost
from src.auth.models import User, TokenData, UserType
from src.models import ConstrainedId
from src.companies.models import Company
from src.crud import (
    add_skills_to_entity_on_create, 
    add_skill_to_entity, 
    remove_skill_from_entity,
    get_entity_by_id
)
from src.job_posts.exceptions import (
    JobPostNotFound, 
    NotAStudent,
    JobApplicationAlreadyExists,
    SkillAlreadyAssignedToJobPost,
    SkillNotAssignedToJobPost,
    JobPostNotSaved,
    JobPostAlreadySaved
)
from src.applications.models import JobApplication, JobApplicationCreate
from src.students.models import Student
from src.keyword_extraction import extract_keywords, create_keywords, sync_keywords

async def get_job_posts(session: AsyncSession):
    result = await session.exec(select(JobPost).where(JobPost.visibility == Visibility.PUBLIC, JobPost.status == JobPostStatus.ONGOING))
    job_posts = result.all()
    return job_posts

async def get_job_post_by_id(session: AsyncSession, job_post_id: int):
    result = await session.exec(select(JobPost).where(JobPost.id == job_post_id))
    job_post = result.first()
    if not job_post:
        raise JobPostNotFound() 
    return job_post

async def student_is_owner(session: AsyncSession, job_post_id: int, student_id: ConstrainedId):
    # Get student job post where student_id is the current user id and job_post_id is the job_post_id
    result = await session.exec(select(StudentJobPost).where(
        (StudentJobPost.student_id == student_id) & 
        (StudentJobPost.job_post_id == job_post_id)))
    student_job_post = result.first()
    if student_job_post is not None:
        return True
    return False

async def is_owner(session: AsyncSession, job_post_id: int, user_id: ConstrainedId, model: Type[SQLModel], foreign_key: str):
    result = await session.exec(select(model).where(
        (getattr(model, foreign_key) == user_id) & 
        (model.job_post_id == job_post_id)))
    job_post = result.first()
    if job_post:
        return True
    return False



async def can_view_job_post(session: AsyncSession, job_post: JobPost, current_user: User, token_data: TokenData):
    if job_post.visibility == Visibility.PUBLIC:
        return True
    if job_post.visibility == Visibility.PRIVATE:
        if job_post.source == "student":
            return await is_owner(
                session, 
                job_post.id, 
                token_data.related_entity_id, 
                StudentJobPost, 
                "student_id")
        if job_post.source == "company":
            return await is_owner(
                session, 
                job_post.id, 
                token_data.related_entity_id,
                CompanyJobPost, 
                "company_id")
    return False

async def add_job_post_skills(
        job_post_id: int, 
        skill_data: list[Dict[str, Any]], 
        session: AsyncSession):
    await add_skills_to_entity_on_create(
        entity_id=job_post_id, 
        entity_model=JobPostSkillTag, 
        skill_data=skill_data, 
        foreign_key="job_post_id",
        session=session
    )



async def create_job_post(
    session: AsyncSession,
    job_post: JobPostCreate,
    entity_id: ConstrainedId,
    job_source: JobSource
):
    if job_source == "student":
        job_post_extra_data = {"source": JobSource.STUDENT, "visibility": Visibility.PRIVATE}
        db_job_post = JobPost.model_validate(job_post, update=job_post_extra_data)
        session.add(db_job_post)
        await session.commit()
        await session.refresh(db_job_post)
        student_job_post_data = {
            "job_post_id": db_job_post.id,
            "student_id": entity_id
        }
        student_job_post = StudentJobPost.model_validate(student_job_post_data)
        session.add(student_job_post)
        await session.commit()
        await session.refresh(student_job_post)
        await session.refresh(db_job_post)
        return db_job_post
        
    
    if job_source == "company":
        job_post_extra_data = {"source": JobSource.COMPANY, "visibility": Visibility.PUBLIC}
        db_job_post = JobPost.model_validate(job_post, update=job_post_extra_data)
        session.add(db_job_post)
        await session.commit()
        await session.refresh(db_job_post)
        company_job_post_data = {
            "job_post_id": db_job_post.id,
            "company_id": entity_id
        }
        company_job_post = CompanyJobPost.model_validate(company_job_post_data)
        session.add(company_job_post)
        await session.commit()
        await session.refresh(company_job_post)
        await session.refresh(db_job_post)
        return db_job_post
        
    
    if job_source== "staff":
        job_post_extra_data = {"source": JobSource.STAFF, "visibility": Visibility.PUBLIC}
        db_job_post = JobPost.model_validate(job_post, update=job_post_extra_data)
        session.add(db_job_post)
        await session.commit()
        await session.refresh(db_job_post)
        return db_job_post


async def create_job_post_full(
        session: AsyncSession,
        job_post: JobPostCreate,
        entity_id: ConstrainedId,
        job_source: JobSource,
):
    db_job_post = await create_job_post(session, job_post, entity_id, job_source)
    await add_job_post_skills(job_post_id=db_job_post.id, skill_data=job_post.skill_data, session=session)
    extracted_keywords = extract_keywords(job_post.description)
    await create_keywords(session, db_job_post.id, "job_post", extracted_keywords)
    await session.commit()
    await session.refresh(db_job_post)
    return db_job_post

async def check_job_post_ownership(
    session: AsyncSession,
    job_post_id: int,
    entity_id: ConstrainedId,
    fk: str,
    model: Type[SQLModel]
):
    
    entity_column = getattr(model, fk)
    result = await session.exec(select(model).where(
        (entity_column == entity_id) & 
        (model.job_post_id == job_post_id)))
    job_post = result.first()
    if job_post is not None:
        return True
    return False

async def update_job_post(
    session: AsyncSession,
    job_post: JobPost,
    update_data: JobPostUpdate
):
    if update_data.description:
        if update_data.description != job_post.description:
            await sync_keywords(session, job_post.id, update_data.description, "job_post")
    job_post_data = update_data.model_dump(exclude_unset=True)
    job_post.sqlmodel_update(job_post_data)
    session.add(job_post)
    await session.commit()
    await session.refresh(job_post)
    return job_post

async def delete_job_post(
        session: AsyncSession,
        job_post: JobPost
):
    return job_post


# get skills for a job post
async def get_job_post_skills(session: AsyncSession, job_post_id: int):
    result = await session.exec(select(JobPostSkillTag).where(JobPostSkillTag.job_post_id == job_post_id))
    job_post_skills = result.all()
    return job_post_skills


# check if an application exists
async def check_application_exists(session: AsyncSession, student_id: ConstrainedId, job_post_id: int):
    result = await session.exec(select(JobApplication).where(
        (JobApplication.student_id == student_id) & 
        (JobApplication.job_post_id == job_post_id)))
    job_application = result.first()
    if job_application is not None:
        return True
    return False

# add an application to a job post
async def add_application_to_job_post(
    session: AsyncSession,
    job_post_id: int,
    job_application: JobApplicationCreate,
    student_id: ConstrainedId,
    commit: bool = True
):
    student = await get_entity_by_id(session=session, entity_id=student_id, entity=Student)
    if student is None:
        raise NotAStudent()
        
    if await check_application_exists(session, student_id, job_post_id):
        raise JobApplicationAlreadyExists()
    
    if await check_job_post_saved(session, student_id, job_post_id) is not None:
        await unsave_job_post(session, job_post_id, student_id)
    
    job_application_extra_data = {"student_id": student_id, "job_post_id": job_post_id}
    if not job_application.date_applied:
        date_applied = datetime.now().date()
        job_application_extra_data["date_applied"] = date_applied
   
    db_job_application = JobApplication.model_validate(
        job_application,
        update=job_application_extra_data)
    session.add(db_job_application)
    if commit:
        await session.commit()
        await session.refresh(db_job_application)
        return db_job_application
    return db_job_application

# get applications for a job post
async def get_job_post_applications(session: AsyncSession, job_post_id: int):
    result = await session.exec(
        select(JobApplication)
        .options(selectinload(JobApplication.student).joinedload(Student.user))
        .where(JobApplication.job_post_id == job_post_id))
    job_applications = result.all()
    return job_applications

# add a skill to a job post
async def add_job_post_skill(
    session: AsyncSession,
    job_post_id: int,
    skill_id: int
):
    await get_job_post_by_id(session=session, job_post_id=job_post_id)
    await add_skill_to_entity(
        skill_tag_base_model=JobPostSkillTag,
        skill_tag_create_model=JobPostSkillTag,
        entity_id=job_post_id,
        skill_id=skill_id,
        foreign_key="job_post_id",
        exception=SkillAlreadyAssignedToJobPost,
        session=session
    )

# remove a skill from a job post
async def remove_job_post_skill(
    session: AsyncSession,
    job_post_id: int,
    skill_id: int
):
    await remove_skill_from_entity(
        entity_id=job_post_id,
        skill_id=skill_id,
        skill_tag_base_model=JobPostSkillTag,
        foreign_key="job_post_id",
        exception=SkillNotAssignedToJobPost,
        session=session
    )
    

async def get_saved_job_posts(session: AsyncSession, student_id: ConstrainedId):
    result = await session.exec(
        select(SavedJobPost).options(selectinload(SavedJobPost.job_post))
        .where(SavedJobPost.student_id == student_id))
    saved_job_posts = result.all()
    return saved_job_posts


async def check_job_post_saved(session: AsyncSession, student_id: ConstrainedId, job_post_id: int):
    result = await session.exec(select(SavedJobPost).where(
        (SavedJobPost.student_id == student_id) & 
        (SavedJobPost.job_post_id == job_post_id)))
    saved_job_post = result.first()
    return saved_job_post 

# save a job post

async def save_job_post(
    session: AsyncSession,
    job_post_id: int,
    student_id: ConstrainedId
):
    
    if await check_application_exists(session, student_id, job_post_id):
        raise JobApplicationAlreadyExists()
    
    if await check_job_post_saved(session, student_id, job_post_id) is not None:
        raise JobPostAlreadySaved()
    
    saved_job_post_data = {"job_post_id": job_post_id, "student_id": student_id}
    saved_job_post = SavedJobPost.model_validate(saved_job_post_data)
    session.add(saved_job_post)
    await session.commit()
    await session.refresh(saved_job_post)
    return saved_job_post

async def unsave_job_post(
    session: AsyncSession,
    job_post_id: int,
    student_id: ConstrainedId
):
    saved_job_post = await check_job_post_saved(session, student_id, job_post_id)
    if saved_job_post is None:
        raise JobPostNotSaved()
    await session.delete(saved_job_post)
    await session.commit()
    return saved_job_post
   
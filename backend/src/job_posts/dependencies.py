from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from fastapi import Depends
from src.students.models import StudentJobPost
from src.companies.models import CompanyJobPost
from src.job_posts.exceptions import JobPostNotFound, JobPostNotVisible
from src.job_posts import service
from src.auth.dependencies import get_token_data, get_current_active_user
from src.auth.models import TokenData, UserType, User
from src.auth.exceptions import AuthorisationFailed

async def get_job_post_by_id(job_post_id: int, session: AsyncSession = Depends(get_session)):
    result = await service.get_job_post_by_id(session=session, job_post_id=job_post_id)
    if result is None:
        raise JobPostNotFound
    return result

async def verify_job_post_read_access(
        job_post_id: int,
        token_data: TokenData = Depends(get_token_data), 
        session: AsyncSession = Depends(get_session)):
    db_job_post = await service.get_job_post_by_id(job_post_id=job_post_id, session=session)

    if db_job_post.visibility == "public":
        return db_job_post
    
    if token_data.user_type in [UserType.ADMIN, UserType.STAFF]:
        return db_job_post
    
    fk = "student_id" if token_data.user_type == UserType.STUDENT else "company_id"
    model = StudentJobPost if token_data.user_type == UserType.STUDENT else CompanyJobPost
    

    if await service.check_job_post_ownership(
        session=session, 
        job_post_id=job_post_id, 
        entity_id=token_data.related_entity_id,
        fk=fk,
        model=model):

        return db_job_post
    raise JobPostNotVisible()
    

async def verify_job_post_access(
        job_post_id: int,
        token_data: TokenData = Depends(get_token_data), 
        session: AsyncSession = Depends(get_session)):
    db_job_post = await service.get_job_post_by_id(job_post_id=job_post_id, session=session)

    if token_data.user_type in [UserType.ADMIN, UserType.STAFF]:
        return db_job_post
    
    fk = "student_id" if token_data.user_type == UserType.STUDENT else "company_id"
    model = StudentJobPost if token_data.user_type == UserType.STUDENT else CompanyJobPost
    

    if await service.check_job_post_ownership(
        session=session, 
        job_post_id=job_post_id, 
        entity_id=token_data.related_entity_id,
        fk=fk,
        model=model):

        return db_job_post
    raise AuthorisationFailed()

async def verify_staff_or_company(
        user: User = Depends(get_current_active_user)):
    if user.user_type in [UserType.STAFF, UserType.ADMIN, UserType.COMPANY]:
        return user
    raise AuthorisationFailed()

async def valid_skill_addition_for_uni_job_post(
        job_post_id: int,
        token_data: TokenData = Depends(get_token_data),
        session: AsyncSession = Depends(get_session)):
    db_job_post = await service.get_job_post_by_id(job_post_id=job_post_id, session=session)
    if db_job_post.source in ["student", "company"]:
        raise AuthorisationFailed()
    if token_data.user_type == UserType.COMPANY:
        raise AuthorisationFailed()
    return db_job_post

async def valid_skill_removal_for_uni_job_post(
        job_post_id: int,
        token_data: TokenData = Depends(get_token_data),
        session: AsyncSession = Depends(get_session)):
    db_job_post = await service.get_job_post_by_id(job_post_id=job_post_id, session=session)
    if db_job_post.source in ["student", "company"]:
        raise AuthorisationFailed()
    if token_data.user_type != UserType.STAFF:
        raise AuthorisationFailed()
    return db_job_post



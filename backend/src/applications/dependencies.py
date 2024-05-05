from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from fastapi import Depends
from src.applications import service
from src.auth.dependencies import get_token_data
from src.auth.models import TokenData, UserType
from src.exceptions import PermissionDenied
from src.applications.exceptions import JobApplicationActivityNotFound
from src.applications.exceptions import JobApplicationNotFound
from src.companies.service import get_company_job_post
from src.applications.models import JobApplicationStage, JobApplicationActivityType
from typing import Union, Annotated
from src.models import ConstrainedId

async def verify_application_access(
        job_application_id: int,
        token_data: TokenData = Depends(get_token_data), 
        session: AsyncSession = Depends(get_session)):
    
    db_job_application = await service.get_job_application_by_id(job_application_id=job_application_id, session=session)
    if db_job_application is None:
        raise JobApplicationNotFound()


    if token_data.user_type in [UserType.ADMIN, UserType.STAFF]:
        return db_job_application
    
    if token_data.user_type == UserType.STUDENT:
        if db_job_application.student_id == token_data.related_entity_id:
            return db_job_application
    
    if token_data.user_type == UserType.COMPANY:
        company_job_post = await get_company_job_post(
            session=session, 
            company_id=token_data.related_entity_id,
            job_post_id=db_job_application.job_post_id)
        if company_job_post is not None:
            return db_job_application

    raise PermissionDenied()


async def verify_activity_access(
        activity_id: int,
        token_data: TokenData = Depends(get_token_data),
        session: AsyncSession = Depends(get_session)):
    activity = await service.get_job_application_activity_by_id(activity_id=activity_id, session=session)
    if activity is None:
        raise JobApplicationActivityNotFound()
    application = await verify_application_access(
        job_application_id=activity.job_application_id, 
        token_data=token_data, 
        session=session)
    if application is None:
        raise PermissionDenied()
    return activity

def application_common_params(
        stage: Union[JobApplicationStage, None] = None,
        student_id: Union[ConstrainedId, None] = None,
        job_post_id: Union[int, None] = None,
        read_job: bool = False
):
    return {
        "stage": stage,
        "student_id": student_id,
        "job_post_id": job_post_id,
        "read_job": read_job
    }

ApplicationCommonsDep = Annotated[dict, Depends(application_common_params)]

def application_activity_common_params(
        job_application_id: Union[int, None] = None,
        activity_type: Union[JobApplicationActivityType, None] = None,
        student_id: Union[ConstrainedId, None] = None,

):
    return {
        "job_application_id": job_application_id,
        "activity_type": activity_type,
    }

ApplicationActivityCommonsDep = Annotated[dict, Depends(application_activity_common_params)]

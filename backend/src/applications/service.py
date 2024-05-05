from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from sqlmodel import select
from src.applications.models import (
    JobApplication, 
    JobApplicationUpdate, 
    JobApplicationActivityCreate,
    JobApplicationActivity,
    JobApplicationActivityUpdate,
    JobApplicationStage,
    JobApplicationActivityType
)
from src.models import ConstrainedId
from src.crud import create_generic, update_generic
from src.applications.exceptions import JobApplicationActivityNotFound
from sqlalchemy.orm import selectinload, joinedload
from src.students.models import Student


async def get_job_applications(
        session: AsyncSession,
        stage: Union[JobApplicationStage, None] = None,
        student_id: Union[ConstrainedId, None] = None,
        job_post_id: Union[int, None] = None,
        read_job: bool = False
    ):
    query = select(JobApplication) 

    if read_job:
        query = query.options(selectinload(JobApplication.job_post))

    conditions = []

    if stage:
        conditions.append(JobApplication.stage == stage)
    if student_id:
        conditions.append(JobApplication.student_id == student_id)
    if job_post_id:
        conditions.append(JobApplication.job_post_id == job_post_id)
    
    query = query.where(*conditions)

    # Sort by date applied
    query = query.order_by(JobApplication.date_applied.desc())

    result = await session.exec(query)
    job_applications = result.all()
    return job_applications


async def get_job_application_by_id(
        job_application_id: int,
        session: AsyncSession):
     # get job application and related job post
    result = await session.exec(
        select(JobApplication)
        .where(JobApplication.id == job_application_id)
        .options(selectinload(JobApplication.activities))
        .options(selectinload(JobApplication.job_post))
        .options(selectinload(JobApplication.student).selectinload(Student.user))
    )

    job_application = result.first()
    
    if job_application:
        job_application.activities = sorted(job_application.activities, key=lambda x: x.date_created, reverse=True)
   
    return job_application


async def update_job_application(
        job_application_id: int,
        session: AsyncSession,
        job_application: JobApplication,
        job_application_update: JobApplicationUpdate):
    
    
    db_application = await update_generic(
        model_id=job_application_id,
        update_data=job_application_update,
        model_getter=get_job_application_by_id,
        session=session
    )
    await session.commit()
    await session.refresh(db_application)
    return await get_job_application_by_id(job_application_id=job_application_id, session=session)

async def get_job_application_activities(
        session: AsyncSession, 
        job_application_id: int, 
        activity_type: Union[JobApplicationActivityType, None] = None,
):
    query = select(JobApplicationActivity).where(JobApplicationActivity.job_application_id == job_application_id)

    if activity_type:
        query = query.where(JobApplicationActivity.activity_type == activity_type)

    query = query.order_by(JobApplicationActivity.date_created.desc())
    
    result = await session.exec(query)
    job_application_activities = result.all()
    return job_application_activities

async def add_job_application_activity(
        job_application_id: int,
        session: AsyncSession,
        job_application_activity: JobApplicationActivityCreate):
    db_job_application = await create_generic(
        model_class=JobApplicationActivity,
        create_data=job_application_activity,
        session=session,
        extra_data={"job_application_id": job_application_id}
    )
    return db_job_application

async def get_job_application_activity_by_id(
        activity_id: int,
        session: AsyncSession):
    result = await session.exec(
        select(JobApplicationActivity).where(JobApplicationActivity.id == activity_id)
    )
    job_application_activity = result.first()
    if job_application_activity is None:
        raise JobApplicationActivityNotFound() 
    return job_application_activity

async def update_job_application_activity(
        activity_id: int,
        session: AsyncSession,
        activity_update: JobApplicationActivityUpdate):
    db_activity =  await update_generic(
        model_id=activity_id,
        update_data=activity_update,
        model_getter=get_job_application_activity_by_id,
        session=session
    )
    await session.commit()
    await session.refresh(db_activity)
    return db_activity

async def delete_job_application_activity(
        activity_id: int,
        session: AsyncSession):
    db_activity = await get_job_application_activity_by_id(activity_id=activity_id, session=session)
    if db_activity is None:
        raise JobApplicationActivityNotFound()
    await session.delete(db_activity)
    await session.commit()

async def get_job_applications_activities(
        session: AsyncSession,
        activity_type: Union[JobApplicationActivityType, None] = None,
        job_application_id: Union[int, None] = None,
        student_id: Union[ConstrainedId, None] = None,
):
    activity_type_list_to_filter = [
        JobApplicationActivityType.intereview,
        JobApplicationActivityType.phone_call,
        JobApplicationActivityType.test,
        JobApplicationActivityType.assessment_center,
    ]

    query = (
        select(JobApplicationActivity)
        .options(
            joinedload(JobApplicationActivity.job_application)
            .selectinload(JobApplication.student)
            .joinedload(Student.user)))
    
    if activity_type:
        query = query.where(JobApplicationActivity.activity_type == activity_type)
    else:
        query = query.where(JobApplicationActivity.activity_type.in_(activity_type_list_to_filter))

    query = query.order_by(JobApplicationActivity.date_created.desc())
    result = await session.exec(query)
    job_application_activities = result.all()
    return job_application_activities
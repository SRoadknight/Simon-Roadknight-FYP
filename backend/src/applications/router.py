from fastapi import APIRouter, Depends, Response, status, Path
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user
from src.auth.models import User
from src.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.applications import service
from src.applications.dependencies import (
    verify_application_access, 
    verify_activity_access, 
    ApplicationCommonsDep,
    ApplicationActivityCommonsDep
)
from src.applications.models import (
    JobApplicationUpdate, 
    JobApplication, 
    JobApplicationActivityRead, 
    JobApplicationActivityCreate,
    JobApplicationActivity,
    JobApplicationActivityUpdate,
    JobApplicationReadWithJob,
    JobApplicationActivityReadFull,
    JobApplicationReadFull

)

router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Staff can view all job applications in the system
@router.get("", response_model=list[JobApplicationReadWithJob])
async def read_job_applications(
    *,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user),
    commons: ApplicationCommonsDep
    ):
    job_applications = await service.get_job_applications(session, **commons)
    return job_applications


# Get all activities for all job applications
@router.get("/upcoming-activities", response_model=list[JobApplicationActivityReadFull])
async def read_all_job_applications_activities(
    commons: ApplicationActivityCommonsDep,
    session: AsyncSession = Depends(get_session),
    _current_user: User = Depends(get_current_active_staff_user) 
    ):
    return await service.get_job_applications_activities(session=session, **commons)


# Get a specific application
@router.get("/{job_application_id}", response_model=JobApplicationReadFull)
async def read_job_application(
    job_application: JobApplication = Depends(verify_application_access)
    ):
    return job_application


# Students and staff can update an existing application 
@router.patch("/{job_application_id}", response_model=JobApplicationReadFull)
async def update_job_application(
    *,
    job_application_id: int,
    job_application: JobApplication = Depends(verify_application_access),
    job_application_update: JobApplicationUpdate,
    session: AsyncSession = Depends(get_session)
    ):
    db_job_application = await service.update_job_application(
        job_application_id=job_application_id,
        session=session,
        job_application=job_application,
        job_application_update=job_application_update)
    
    return db_job_application
    

# Delete a job application, this is not implemented
# Will require the deletion of activities and other related data too




# Get all activities for a job application
@router.get("/{job_application_id}/activities")
async def read_job_application_activities(
    commons: ApplicationActivityCommonsDep,
    job_application: JobApplication = Depends(verify_application_access),
    session: AsyncSession = Depends(get_session)
    ):
    commons["job_application_id"] = job_application.id
    return await service.get_job_application_activities(session=session, **commons)

# Get a specific activity for a job application
@router.get("/activities/{activity_id}")
async def read_job_application_activity(
    *,
    job_application_activity: JobApplicationActivity = Depends(verify_activity_access),
    session: AsyncSession = Depends(get_session)
    ):
    return await service.get_job_application_activity_by_id(
        session=session,
        activity_id=job_application_activity.id)



# Add a job application activity
@router.post("/{job_application_id}/activities", response_model=JobApplicationActivityRead)
async def add_job_application_activity(
    *,
    job_application: JobApplication = Depends(verify_application_access),
    activity: JobApplicationActivityCreate,
    session: AsyncSession = Depends(get_session)
    ):
    activity = await service.add_job_application_activity(
        session=session,
        job_application_id=job_application.id,
        job_application_activity=activity) 
    return activity 

# Update a job application activity
@router.patch("/activities/{activity_id}")
async def update_job_application_activity(
    *,
    job_application_activity: JobApplicationActivity = Depends(verify_activity_access),
    activity_update: JobApplicationActivityUpdate,
    session: AsyncSession = Depends(get_session)
    ):
    activity = await service.update_job_application_activity(
        session=session,
        activity_id=job_application_activity.id,
        activity_update=activity_update)
    return activity

# Delete a job application activity
@router.delete("/activities/{activity_id}")
async def delete_job_application_activity(
    *,
    job_application_activity: JobApplicationActivity = Depends(verify_activity_access),
    session: AsyncSession = Depends(get_session)
    ):
    await service.delete_job_application_activity(
        session=session,
        activity_id=job_application_activity.id)
    return Response(status_code=status.HTTP_200_OK)


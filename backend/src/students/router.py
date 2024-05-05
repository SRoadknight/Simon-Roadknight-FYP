from fastapi import APIRouter, Depends, Response, status
from src.students.models import (
    StudentReadWithUser,
    Student, 
    StudentUpdate, 
    ExternalProfileCreate,
    ExternalProfile,
    ExternalProfileUpdate,
    StudentActivityCreate,
    StudentActivityUpdate,
    StudentActivityRead,
    StudentActivity,
    StudentDegreeRead,
)

from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user, get_token_data, get_current_active_student_user
from src.auth.models import User, TokenData
from src.students import service
from src.students.dependencies import (
    verify_external_profile_access,
    verify_activity_access,
    StudentActivityCommonsDep
)
from src.models import ConstrainedId
from src.applications.models import JobApplicationReadWithJob, StudentJobPostApplicationCreate
from src.job_posts.models import JobPostRead, JobPost, JobPostUpdate
from src.job_posts.dependencies import verify_job_post_access
from src.job_posts.dependencies import verify_job_post_access
from src.events.models import EventRead, EventReadWithSkills
from src.events.dependencies import EventCommonsDep
from typing import Union
from src.groups.models import GroupRead
from src.interactions.service import update_interaction as student_update_interaction
from src.interactions.models import StudentInteractionUpdate, InteractionReadWithStaff, InteractionCreate, InteractionReadWithStudent, InteractionReadWithStudentAndStaff
from src.interactions.dependencies import verify_interaction_modify_access
from src.recommendations import get_recommended_jobs
from src.applications.dependencies import ApplicationCommonsDep
from src.interactions.dependencies import InteractionCommonsDep
from src.appointments.dependencies import AppointmentCommonsDep

router = APIRouter(dependencies=[Depends(get_current_active_user)])

# get all students (not disabled)
@router.get("", response_model=list[StudentReadWithUser])
async def read_students(
    current_user: User = Depends(get_current_active_staff_user),
    session: AsyncSession = Depends(get_session),
    disabled: bool = False
    ):
    students = await service.get_students(session, disabled=disabled)
    return students

""" # create a new student
@router.post("", response_model=StudentRead)
async def create_student(
    *,
    session: AsyncSession = Depends(get_session),
    student: StudentUserCreate = Depends(valid_student_create),
    current_user: User = Depends(get_current_active_staff_user)
    ):
    student = await service.create_student(session=session, student=student)
    return student """

# student gets their own profile
@router.get("/me", response_model=StudentReadWithUser)
async def get_own_student_profile(
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
    ):
    student = await service.get_student_with_user(session=session, student_id=token_data.related_entity_id)
    return student

# student updates their own profile
@router.patch("/me", response_model=StudentReadWithUser)
async def update_own_student_profile(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    student_update: StudentUpdate,
    session: AsyncSession = Depends(get_session)
    ):
    student = await service.update_student(
        session=session, 
        student_update=student_update, 
        student_id=token_data.related_entity_id
    )
    return student

# get a list of external profiles for a student
@router.get("/me/external-profiles")
async def get_own_student_external_profiles(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    profiles = await service.get_student_external_profiles(session=session, student_id=token_data.related_entity_id)
    return profiles


# get a list of degrees a student is studying or has studied
@router.get("/me/degrees", response_model=list[StudentDegreeRead])
async def get_own_student_degrees(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    degrees = await service.get_student_degrees(session=session, student_id=token_data.related_entity_id)
    return degrees

# get a list of skill tags for a student
@router.get("/me/skill-tags")
async def get_own_student_skill_tags(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    skills = await service.get_student_skill_tags(session=session, student_id=token_data.related_entity_id)
    return skills


# get a list of job posts a student has created
@router.get("/me/job-posts", response_model=list[JobPostRead])
async def get_own_student_job_posts(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    job_posts = await service.get_student_job_posts(session=session, student_id=token_data.related_entity_id)
    return job_posts

# get a students job applications
@router.get("/me/job-applications", response_model=list[JobApplicationReadWithJob])
async def get_own_student_job_applications(
    commons: ApplicationCommonsDep,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    commons["student_id"] = token_data.related_entity_id
    commons["read_job"] = True
    job_applications = await service.get_student_job_applications(session=session, commons=commons)
    return job_applications


#  get a list of events a student has registered for
@router.get("/me/events", response_model=list[EventReadWithSkills])
async def get_own_student_events(
    *,
    commons: EventCommonsDep,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    commons["student_id"] = token_data.related_entity_id
    events = await service.get_student_events(session=session, commons=commons)
    return events


# get a list of appointments a student has booked
@router.get("/me/appointments")
async def get_own_student_appointments(
    *,
    commons: AppointmentCommonsDep,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):

    commons["student_id"] = token_data.related_entity_id
    appointments = await service.get_student_appointments(session=session, commons=commons)
    return appointments



# Get a list of groups a student is a member of
@router.get("/me/groups", response_model=list[GroupRead])
async def get_own_student_group_membership(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    groups = await service.get_student_group_membership(session=session, student_id=token_data.related_entity_id)
    return groups


# Get a list of a students interactions
@router.get("/me/interactions", response_model=list[InteractionReadWithStaff])
async def get_own_student_interactions(
    *,
    commons: InteractionCommonsDep,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    commons["student_id"] = token_data.related_entity_id
    commons["read_staff"] = True
    interactions = await service.get_student_interactions(session=session, commons=commons)
    return interactions

# Get recommended jobs for a student 
@router.get("/me/recommended-jobs", response_model=list[JobPostRead])
async def get_own_student_recommended_jobs(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    job_posts = await get_recommended_jobs(session=session, student_id=token_data.related_entity_id)
    return job_posts

# Get a list of a students activties 
@router.get("/me/activities", response_model=list[StudentActivityRead])
async def get_own_student_activities(
    *,
    commons: StudentActivityCommonsDep,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    commons["student_id"] = token_data.related_entity_id
    activities = await service.get_student_activities(session=session, **commons)
    return activities

# add an external profile to a student
@router.post("/external-profiles")
async def add_external_profile_to_student(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    profile: ExternalProfileCreate,
    session: AsyncSession = Depends(get_session)
):
    return await service.add_external_profile_to_student(
        session=session, 
        profile=profile,
        student_id=token_data.related_entity_id)


# Students can add an activity
@router.post("/activities", response_model=StudentActivityRead)
async def add_student_activity(
    activity: StudentActivityCreate,
    token_data: TokenData = Depends(get_current_active_student_user),
    session: AsyncSession = Depends(get_session)
):
    return await service.create_student_activity(
        session=session, 
        activity=activity, 
        student_id=token_data.related_entity_id)


# Staff and students can update a students external profile
@router.patch("/external-profiles/{external_profile_id}")
async def update_external_profile(
    *,
    external_profile: ExternalProfile = Depends(verify_external_profile_access),
    update_data: ExternalProfileUpdate,
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(get_token_data)
):
    return await service.update_external_profile(
        session=session, 
        external_profile=external_profile, 
        update_data=update_data,
        student_id=token_data.related_entity_id)

# Staff and students can update a students activity
@router.patch("/activities/{activity_id}")
async def update_student_activity(
    *,
    activity: StudentActivity = Depends(verify_activity_access),
    update_data: StudentActivityUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await service.update_student_activity(
        activity_id=activity.id,
        session=session, 
        update_data=update_data)

# remove an external profile from a student
@router.delete("/external-profiles/{external_profile_id}")
async def remove_external_profile_from_student(
    *,
    external_profile: ExternalProfile = Depends(verify_external_profile_access),
    session: AsyncSession = Depends(get_session)
):
    await service.remove_external_profile_from_student(
        session=session, 
        external_profile=external_profile)
    
    return Response(status_code=status.HTTP_200_OK)

# Staff and students can delete a students activity
@router.delete("/activities/{activity_id}")
async def remove_student_activity(
    *,
    activity: StudentActivity = Depends(verify_activity_access),
    session: AsyncSession = Depends(get_session)
):
    await service.remove_student_activity(
        session=session, 
        activity_id=activity.id)
    
    return Response(status_code=status.HTTP_200_OK)


# add a skill tag to a student
@router.post("/skill-tags/{skill_id}")
async def add_skill_tag_to_student(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    skill_id: int,
    session: AsyncSession = Depends(get_session)
):
    await service.add_skill_tag_to_student(
        session=session, 
        student_id=token_data.related_entity_id, 
        skill_id=skill_id)
    return Response(status_code=status.HTTP_200_OK)

# remove a skill tag from a student
@router.delete("/skill-tags/{skill_id}")
async def remove_skill_tag_from_student(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    skill_id: int,
    session: AsyncSession = Depends(get_session)
):
    await service.remove_skill_tag_from_student(
        session=session, 
        student_id=token_data.related_entity_id, 
        skill_id=skill_id)
    return Response(status_code=status.HTTP_200_OK)


# Create a job post, student job post and link an application to the job post
@router.post("/job-posts", response_model=JobApplicationReadWithJob) 
async def create_job_post_and_application(
    *,
    token_data: TokenData = Depends(get_current_active_student_user),
    job_post_application: StudentJobPostApplicationCreate,
    session: AsyncSession = Depends(get_session)
):
    job_post_with_application = await service.create_student_job_post_and_application(
        session=session, 
        job_post_application=job_post_application, 
        student_id=token_data.related_entity_id)
    return job_post_with_application

# update a students job post - both staff and student can update a students job post
# using this endpoint
@router.patch("/job-posts/{job_post_id}")
async def update_student_job_post(
    *,
    job_post_id: int,
    job_post: JobPost = Depends(verify_job_post_access),
    job_post_update: JobPostUpdate,
    session: AsyncSession = Depends(get_session)
):
    db_job_post = await service.update_student_job_post(
        session=session, 
        job_post=job_post, 
        job_post_update=job_post_update)
    return db_job_post

# Update a students interaction to leave or update feedback
@router.patch("/interactions/{interaction_id}", response_model=Union[InteractionReadWithStaff, InteractionReadWithStudent])
async def update_interaction(
    interaction_id: int,
    interaction: StudentInteractionUpdate,
    _: TokenData = Depends(verify_interaction_modify_access),
    session: AsyncSession = Depends(get_session)
):
    interaction = await student_update_interaction(
        interaction_id=interaction_id,
        interaction=interaction,
        session=session,
        student=True
    )
    return interaction

# add a skill tag to a student job post
@router.post("/job-posts/{job_post_id}/skill-tags/{skill_id}")
async def add_skill_tag_to_student_job_post(
    *,
    job_post: JobPost = Depends(verify_job_post_access),
    job_post_id: int,
    skill_id: int,
    session: AsyncSession = Depends(get_session)
):
    await service.add_skill_tag_to_student_job_post(
        session=session, 
        job_post_id=job_post_id, 
        skill_id=skill_id)
    return Response(status_code=status.HTTP_200_OK)

# remove a skill tag from a student job post
@router.delete("/job-posts/{job_post_id}/skill-tags/{skill_id}")
async def remove_skill_tag_from_student_job_post(
    *,
    job_post: JobPost = Depends(verify_job_post_access),
    job_post_id: int,
    skill_id: int,
    session: AsyncSession = Depends(get_session)
):
    await service.remove_skill_tag_from_student_job_post(
        session=session, 
        job_post_id=job_post_id, 
        skill_id=skill_id)
    return Response(status_code=status.HTTP_200_OK)




# delete a students job post
# this needs to delete the the job post and student job post 
# and any applications linked to the job post 
# and any activities linked to the application


# get student by id
@router.get("/{student_id}", response_model=StudentReadWithUser)
async def get_student_by_id(
    *,
    current_user: Student = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
    ):
    student = await service.get_student_with_user(session=session, student_id=student_id)
    return student

# update a student as a staff member
@router.patch("/{student_id}", response_model=StudentReadWithUser)
async def update_student(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session),
    student_update: StudentUpdate
    ):
    student = await service.update_student(
        session=session, 
        student_id=student_id, 
        student_update=student_update)
    return student

# get a list of external profiles for a student
@router.get("/{student_id}/external-profiles")
async def get_student_external_profiles(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    profiles = await service.get_student_external_profiles(session=session, student_id=student_id)
    return profiles

# get a list of degrees a student is studying or has studied
@router.get("/{student_id}/degrees", response_model=list[StudentDegreeRead])
async def get_student_degrees(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    degrees = await service.get_student_degrees(session=session, student_id=student_id)
    return degrees

# get a list of skill tags for a student
@router.get("/{student_id}/skill-tags")
async def get_student_skill_tags(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    skills = await service.get_student_skill_tags(session=session, student_id=student_id)
    return skills

# get a students job applications
@router.get("/{student_id}/job-applications", response_model=list[JobApplicationReadWithJob])
async def get_student_job_applications(
    *,
    commons: ApplicationCommonsDep,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    commons["student_id"] = student_id
    commons["read_job"] = True
    job_applications = await service.get_student_job_applications(session=session, commons=commons)
    return job_applications

# get a list of events a student has registered for
@router.get("/{student_id}/events", response_model=list[EventRead])
async def get_student_events(
    *,
    commons: EventCommonsDep,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    commons["student_id"] = student_id
    events = await service.get_student_events(session=session, commons=commons)
    return events

# get a list of appointments a student has booked
@router.get("/{student_id}/appointments")
async def get_student_appointments(
    *,
    commons: AppointmentCommonsDep,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    commons["student_id"] = student_id
    appointments = await service.get_student_appointments(session=session, commons=commons)
    return appointments

# get a list of job posts a student has created
@router.get("/{student_id}/job-posts", response_model=list[JobPostRead])
async def get_student_job_posts(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    job_posts = await service.get_student_job_posts(session=session, student_id=student_id)
    return job_posts

# Get a list of groups a student is a member of
@router.get("/{student_id}/groups", response_model=list[GroupRead])
async def get_student_group_membership(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    groups = await service.get_student_group_membership(session=session, student_id=student_id)
    return groups


# Get a list of student and staff interactions
@router.get("/{student_id}/interactions", response_model=list[InteractionReadWithStudentAndStaff])
async def get_student_interactions(
    *,
    commons: InteractionCommonsDep,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    commons["student_id"] = student_id
    commons["read_student"] = True
    commons["read_staff"] = True
    interactions = await service.get_student_interactions(session=session, commons=commons)
    return interactions

# get a list of a students activties
@router.get("/{student_id}/activities", response_model=list[StudentActivityRead])
async def get_student_activities(
    *,
    commons: StudentActivityCommonsDep,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    commons["student_id"] = student_id
    activities = await service.get_student_activities(session=session, **commons)
    return activities

# Staff can add a student activity
@router.post("/{student_id}/activities", response_model=StudentActivityRead)
async def add_student_activity(
    *,
    _current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    activity: StudentActivityCreate,
    session: AsyncSession = Depends(get_session)
):
    return await service.create_student_activity(
        session=session, 
        activity=activity, 
        student_id=student_id)

# Add an interaction to a student
@router.post("/{student_id}/interactions", response_model=InteractionReadWithStaff)
async def add_interaction_to_student(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    interaction: InteractionCreate,
    session: AsyncSession = Depends(get_session)
):
    return await service.create_student_interaction(
        session=session, 
        interaction=interaction, 
        student_id=student_id,
        career_staff_id=current_user.related_entity_id)


# careers staff add a job post for the student and link an application to the job post
@router.post("/{student_id}/job-posts", response_model=JobApplicationReadWithJob)
async def create_job_post_and_application(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    job_post_application: StudentJobPostApplicationCreate,
    session: AsyncSession = Depends(get_session)
):
    job_post = await service.create_student_job_post_and_application(
        session=session, 
        job_post_application=job_post_application, 
        student_id=student_id)
    return job_post


# Careers staff can see jobs recommended to a student
@router.get("/{student_id}/recommended-jobs", response_model=list[JobPostRead])
async def get_student_recommended_jobs(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    job_posts = await get_recommended_jobs(session=session, student_id=student_id)
    return job_posts


# careers staff can add skill tags to a student
@router.post("/{student_id}/skill-tags/{skill_id}")
async def add_skill_tag_to_student(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    skill_id: int,
    session: AsyncSession = Depends(get_session)
):
    await service.add_skill_tag_to_student(session=session, student_id=student_id, skill_id=skill_id)
    return Response(status_code=status.HTTP_200_OK)

# careers staff can remove a skill tag from a student
@router.delete("/{student_id}/skill-tags/{skill_id}")
async def remove_skill_tag_from_student(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    skill_id: int,
    session: AsyncSession = Depends(get_session)
):
    await service.remove_skill_tag_from_student(session=session, student_id=student_id, skill_id=skill_id)
    return Response(status_code=status.HTTP_200_OK)


# link a student to a degree
@router.post("/{student_id}/degrees/{degree_code}")
async def add_degree_to_student(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    degree_code: str,
    session: AsyncSession = Depends(get_session)
):
    await service.add_degree_to_student(session=session, student_id=student_id, degree_code=degree_code)
    return Response(status_code=status.HTTP_200_OK)

# remove a degree from a student
@router.delete("/{student_id}/degrees/{degree_code}")
async def remove_degree_from_student(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    student_id: ConstrainedId,
    degree_code: str,
    session: AsyncSession = Depends(get_session)
):
    await service.remove_degree_from_student(session=session, student_id=student_id, degree_code=degree_code)
    return Response(status_code=status.HTTP_200_OK)





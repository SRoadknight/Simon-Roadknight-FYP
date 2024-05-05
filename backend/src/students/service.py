from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.students.models import (
    Student,
    StudentUserCreate,
    StudentUpdate, 
    StudentDegree, 
    StudentDegreeCreate,
    ExternalProfileCreate,
    ExternalProfile,
    ExternalProfileUpdate,
    StudentSkillTag,
    StudentSkillTagCreate,
    StudentJobPost,
    StudentActivity,
    StudentActivityCreate,
    StudentActivityUpdate
)
from src.auth.models import User
from src.crud import create_generic, update_generic, add_skill_to_entity, remove_skill_from_entity
from src.auth.service import (
    create_user, 
    get_user_by_entity_id, 
    disable_user_account,
    enable_user_account)
from src.students.exceptions import (
    StudentNotFound, 
    StudentDegreeAlreadyExists, 
    StudentDegreeNotFound,
    ExternalProfileAlreadyExists,
    ExternalProfileNotFound,
    SkillTagAlreadyExists,
    SkillTagNotAttached,
    ActivityNotFound
)
from src.models import ConstrainedId
from src.degrees.service import get_degree_by_code
from sqlmodel import SQLModel
from src.job_posts.service import (
    create_job_post_full, 
    update_job_post, 
    add_application_to_job_post,
    get_job_post_by_id,
    add_job_post_skill,
    remove_job_post_skill
    
)
from src.job_posts.models import JobPostCreate, JobPost, JobPostUpdate, JobSource
from src.applications.models import JobApplicationCreate, StudentJobPostApplicationCreate
from sqlalchemy.orm import joinedload
from src.job_posts.exceptions import JobPostNotFound
from src.events.service import get_events
from sqlalchemy import or_
from typing import Union
from src.groups.models import GroupMember, Group
from src.interactions.models import Interaction, InteractionCreate
from src.keyword_extraction import extract_keywords, create_keywords, sync_keywords
from src.events.dependencies import EventCommonsDep
from src.applications.dependencies import ApplicationCommonsDep
from src.applications.service import get_job_applications, get_job_application_by_id
from src.interactions.service import get_interactions
from src.interactions.dependencies import InteractionCommonsDep
from src.appointments.service import get_appointments
from src.appointments.dependencies import AppointmentCommonsDep


async def get_students(session: AsyncSession, disabled: bool = False):
    # Select students with thier user details
    result = await session.exec(
        select(Student)
        .options(joinedload(Student.user))
        .where(Student.user_id == User.id, User.disabled == disabled)
    )
    students = result.all()
    return students

async def get_student_by_id(student_id: ConstrainedId, session: AsyncSession):
    result = await session.exec(
        select(Student).where(Student.id == student_id)
    )
    student = result.first()
    return student

async def get_student_with_user(session: AsyncSession, student_id: ConstrainedId):
    result = await session.exec(
        select(Student)
        .options(joinedload(Student.user))
        .where(Student.id == student_id)
    )
    student = result.first()
    if student is None:
        raise StudentNotFound()
    return student

async def create_student(session: AsyncSession, student: StudentUserCreate):
    db_student_user = await create_user(
        user=student,
        session=session
    )
    student = await create_generic(
        model_class=Student,
        create_data=student,
        session=session,
        extra_data={"user_id": db_student_user.id}
    )
    if student.about is not None:
        extracted_keywords = extract_keywords(student.about)
        await create_keywords(session, student.id, "Student", extracted_keywords)
    await session.commit()
    await session.refresh(student)
    return student


async def update_student(
        session: AsyncSession, 
        student_update: StudentUpdate,
        student_id: ConstrainedId):
    
    student = await get_student_by_id(student_id, session)
    if student is None:
        raise StudentNotFound()
    
    if student_update.about:
        if student.about != student_update.about:
            await sync_keywords(session, student_id, student_update.about, "Student")


    student_update_data = student_update.model_dump(exclude_unset=True)
    student.sqlmodel_update(student_update_data)
    session.add(student)
    await session.commit()
    await session.refresh(student)
    return await get_student_with_user(session, student_id)
    

async def disable_student(
        session: AsyncSession, 
        student_id: ConstrainedId):
    user = await get_user_by_entity_id(
        student_id, 
        session, 
        Student, 
        exception=StudentNotFound)
    await disable_user_account(session, user)


async def enable_student(
        session: AsyncSession, 
        student_id: ConstrainedId):
    user = await get_user_by_entity_id(
        student_id, 
        session, 
        Student, 
        exception=StudentNotFound)
    await enable_user_account(session, user)

async def check_if_student_linked_to_degree(
        session: AsyncSession, 
        student_id: ConstrainedId, 
        degree_code: str):
    result = await session.exec(
        select(StudentDegree)
        .where(StudentDegree.student_id == student_id, 
               StudentDegree.degree_code == degree_code)
    )
    student_degree = result.first()
    return student_degree is not None

async def add_degree_to_student(
        session: AsyncSession, 
        student_id: ConstrainedId, 
        degree_code: str):
    
    student = get_student_by_id(student_id, session)
    if student is None:
        raise StudentNotFound()
    
    await get_degree_by_code(degree_code, session)
    # check whether student has already been linked to degree
    if await check_if_student_linked_to_degree(session, student_id, degree_code):
        raise StudentDegreeAlreadyExists()



    student_degree_data = {"student_id": student_id, "degree_code": degree_code}
    db_degree_data = await create_generic(
        model_class=StudentDegree,
        create_data=StudentDegreeCreate(**student_degree_data),
        session=session
    )
    return db_degree_data


async def remove_degree_from_student(
        session: AsyncSession, 
        student_id: ConstrainedId, 
        degree_code: str):
    
    student = get_student_by_id(student_id, session)
    if student is None:
        raise StudentNotFound()
    await get_degree_by_code(degree_code, session)

    if not await check_if_student_linked_to_degree(session, student_id, degree_code):
        raise StudentDegreeNotFound()
    
   

    result = await session.exec(
        select(StudentDegree)
        .where(StudentDegree.student_id == student_id, 
               StudentDegree.degree_code == degree_code)
    )
    student_degree = result.first()
    await session.delete(student_degree)
    await session.commit()


async def get_external_profile_by_id(
        session: AsyncSession, 
        external_profile_id: int):
    
    result = await session.exec(
        select(ExternalProfile).where(ExternalProfile.id == external_profile_id)
    )
    external_profile = result.first()
    if external_profile is None:
        raise ExternalProfileNotFound()
    return external_profile


async def check_if_student_has_external_profile(
        session: AsyncSession, 
        student_id: ConstrainedId, 
        external_profile: SQLModel,
        update_data: Union[None, ExternalProfileUpdate] = None):
    
    if update_data:
        result = await session.exec(
            select(ExternalProfile)
            .where(ExternalProfile.student_id == student_id,
                   ExternalProfile.id != external_profile.id,
                     or_(
                          ExternalProfile.website_url == update_data.website_url,
                          ExternalProfile.website == update_data.website
                     )
            )
        )
        external_profile = result.first()
        return external_profile is not None
    
    result = await session.exec(
        select(ExternalProfile)
        .where(ExternalProfile.student_id == student_id,
        or_(
            ExternalProfile.website_url == external_profile.website_url,
            ExternalProfile.website == external_profile.website
            )
        )
    )
    external_profile = result.first()
    return external_profile is not None

async def add_external_profile_to_student(
        session: AsyncSession, 
        student_id: ConstrainedId, 
        profile: ExternalProfileCreate):
    
    if await check_if_student_has_external_profile(
        session, 
        student_id, 
        profile):
        raise ExternalProfileAlreadyExists()
    
    return await create_generic(
        model_class=ExternalProfile,
        create_data=profile,
        session=session,
        extra_data={"student_id": student_id}
    )


async def update_external_profile(
        session: AsyncSession, 
        external_profile: ExternalProfile, 
        update_data: ExternalProfileUpdate,
        student_id: ConstrainedId):
    
    
    if await check_if_student_has_external_profile(
        session, 
        student_id, 
        external_profile,
        update_data=update_data):
        raise ExternalProfileAlreadyExists()
    
    external_profile_data = update_data.model_dump(exclude_unset=True)
    db_external_profile = external_profile.sqlmodel_update(external_profile_data)
    session.add(db_external_profile)
    await session.commit()
    await session.refresh(db_external_profile)
    return db_external_profile



async def remove_external_profile_from_student(
        session: AsyncSession, 
        external_profile: ExternalProfile):
    await session.delete(external_profile)
    await session.commit()

    
# add a skill tag to a student
async def add_skill_tag_to_student(
        session: AsyncSession, 
        student_id: ConstrainedId, 
        skill_id: int):
    return await add_skill_to_entity(
        skill_tag_base_model=StudentSkillTag,
        skill_tag_create_model=StudentSkillTagCreate,
        entity_id=student_id,
        skill_id=skill_id,
        foreign_key="student_id",
        exception=SkillTagAlreadyExists,
        session=session)



# remove a skill tag from a student
async def remove_skill_tag_from_student(
        session: AsyncSession, 
        student_id: ConstrainedId, 
        skill_id: int):
    await remove_skill_from_entity(
        skill_tag_base_model=StudentSkillTag,
        entity_id=student_id,
        skill_id=skill_id,
        foreign_key="student_id",
        exception=SkillTagNotAttached,
        session=session)
    

async def get_student_external_profiles(session: AsyncSession, student_id: ConstrainedId):
    result = await session.exec(
        select(ExternalProfile).where(ExternalProfile.student_id == student_id)
    )
    external_profiles = result.all()
    return external_profiles
    
async def get_student_degrees(session: AsyncSession, student_id: ConstrainedId):
    result = await session.exec(
        select(StudentDegree)
        .where(StudentDegree.student_id == student_id)
        .options(joinedload(StudentDegree.degree))
    )
    student_degrees = result.all()
    return student_degrees

async def get_student_skill_tags(session: AsyncSession, student_id: ConstrainedId):
    result = await session.exec(
        select(StudentSkillTag).where(StudentSkillTag.student_id == student_id)
    )
    student_skill_tags = result.all()
    return student_skill_tags

async def get_student_job_applications(session: AsyncSession, commons: ApplicationCommonsDep):
    job_applications = await get_job_applications(session=session, **commons)
    return job_applications

async def get_student_events(session: AsyncSession, commons: EventCommonsDep):
    events = await get_events(session=session, **commons)
    return events

async def get_student_interactions(
        session: AsyncSession, 
        commons: InteractionCommonsDep
    ):
    interactions = await get_interactions(session=session, **commons)
    return interactions
    

async def get_student_appointments(
        session: AsyncSession,
        commons: AppointmentCommonsDep
    ):

    appointments = await get_appointments(session=session, **commons)
    return appointments


async def get_student_job_posts(
        session: AsyncSession, 
        student_id: ConstrainedId):
    student = await get_student_by_id(student_id, session)
    if student is None:
        raise StudentNotFound()
    
    result = await session.exec(
        select(JobPost)
        .join(StudentJobPost, JobPost.id == StudentJobPost.job_post_id)
        .where(StudentJobPost.student_id == student_id)
    )
    student_job_posts = result.all()
    return student_job_posts


async def get_student_group_membership(
        session: AsyncSession, 
        student_id: ConstrainedId):
    student = await get_student_by_id(student_id, session)
    if student is None:
        raise StudentNotFound()
    
    result = await session.exec(
        select(Group)
        .join(GroupMember)
        .where(GroupMember.student_id == student_id)
    )
    group_membership = result.all()
    return group_membership

    

async def get_student_activities(
        session: AsyncSession, 
        student_id: ConstrainedId,
        activity_type: Union[None, str] = None
    ):
    
   
    student = await get_student_by_id(student_id, session)
    if student is None:
        raise StudentNotFound()
    
    query = select(StudentActivity)

    conditions = []

    if activity_type:
        conditions.append(StudentActivity.activity_type == activity_type)
    
    conditions.append(StudentActivity.student_id == student_id)
    
    query = query.where(*conditions)

    result = await session.exec(query)
    activities = result.all()
    return activities

async def get_student_activity_by_id(
        activity_id: int,
        session: AsyncSession):
    result = await session.exec(
        select(StudentActivity).where(StudentActivity.id == activity_id)
    )
    activity = result.first()
    return activity

async def create_student_activity(
        session: AsyncSession, 
        student_id: ConstrainedId, 
        activity: StudentActivityCreate):
    return await create_generic(
        model_class=StudentActivity,
        create_data=activity,
        session=session,
        extra_data={"student_id": student_id}
    )


async def create_student_interaction(
        session: AsyncSession, 
        student_id: ConstrainedId, 
        career_staff_id: ConstrainedId,
        interaction: InteractionCreate):
    return await create_generic(
        model_class=Interaction,
        create_data=interaction,
        session=session,
        extra_data={"student_id": student_id, "careers_staff_id": career_staff_id}
    )

async def update_student_activity(
        activity_id: int,
        session: AsyncSession,
        update_data: StudentActivityUpdate):
    
    db_updated_activity = await update_generic(
        model_id=activity_id,
        update_data=update_data,
        model_getter=get_student_activity_by_id,
        session=session
    )
    await session.commit()
    await session.refresh(db_updated_activity)
    return db_updated_activity

async def remove_student_activity(
        session: AsyncSession,
        activity_id: int):
    activity = await get_student_activity_by_id(activity_id, session)
    if activity is None:
        raise ActivityNotFound()
    await session.delete(activity)
    await session.commit()

    




async def create_student_job_post_and_application(
        session: AsyncSession, 
        job_post_application: StudentJobPostApplicationCreate,
        student_id: ConstrainedId):
    
    # create the job post 
    job_post: JobPostCreate = JobPostCreate.model_validate(job_post_application)
    db_job_post = await create_job_post_full(
        session=session, 
        job_post=job_post, 
        entity_id=student_id,
        job_source=JobSource.STUDENT)
    
    # create the job post application
    job_application = JobApplicationCreate.model_validate(job_post_application)
    db_job_application = await add_application_to_job_post(
        session=session, 
        job_post_id=db_job_post.id, 
        job_application=job_application,
        student_id=student_id,
        commit=False)
    
    await session.commit()
    await session.refresh(db_job_application)
    db_job_post_with_application =  await get_job_application_by_id(session=session, job_application_id=db_job_application.id)
    return db_job_post_with_application
    

# update student job post
async def update_student_job_post(
    session: AsyncSession, 
    job_post: JobPost, 
    job_post_update: JobPostUpdate):
    
    db_job_post = await update_job_post(
        session=session, 
        job_post=job_post, 
        update_data=job_post_update
    )

    return db_job_post



# add skill to student job post 
async def add_skill_tag_to_student_job_post(
        session: AsyncSession, 
        job_post_id: int, 
        skill_id: int):

    job_post = await get_job_post_by_id(session=session, job_post_id=job_post_id)
    if job_post is None:
        raise JobPostNotFound()
    
    await add_job_post_skill(
        session=session, 
        job_post_id=job_post_id, 
        skill_id=skill_id
    )

# remove skill from student job post
async def remove_skill_tag_from_student_job_post(
        session: AsyncSession, 
        job_post_id: int, 
        skill_id: int):
    job_post = await get_job_post_by_id(session=session, job_post_id=job_post_id)
    if job_post is None:
        raise JobPostNotFound()
    
    await remove_job_post_skill(
        session=session, 
        job_post_id=job_post_id, 
        skill_id=skill_id
    )

    

    

        

    

        

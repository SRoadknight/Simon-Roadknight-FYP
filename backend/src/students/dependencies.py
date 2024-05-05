from fastapi import Depends
from src.auth.dependencies import get_token_data
from src.auth.service import get_user_by_email
from src.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.students import service
from src.auth.models import TokenData, UserType
from src.students.exceptions import StudentNotFound, StudentAlreadyRegistered, ActivityNotFound
from src.auth.exceptions import AuthorisationFailed
from src.students.models import StudentUserCreate, ActivityType
from src.models import ConstrainedId
from typing import Annotated, Union

async def valid_student_create(
    student_create: StudentUserCreate,
    session: AsyncSession = Depends(get_session)
):
    if await get_user_by_email(student_create.email_address, session):
        raise StudentAlreadyRegistered()
    student = await service.get_student_by_id(student_create.id, session)
    if student is not None:
        raise StudentAlreadyRegistered()
    return student_create

async def verify_student_profile_access(
    token_data: TokenData = Depends(get_token_data),
    session: AsyncSession = Depends(get_session)
):
    if token_data.user_type != "student":
        raise AuthorisationFailed()
    student = await service.get_student_by_id(token_data.related_entity_id, session)
    if student is None:
        raise StudentNotFound()
    return student


async def verify_external_profile_access(
    external_profile_id: int,
    token_data: TokenData = Depends(get_token_data),
    session: AsyncSession = Depends(get_session)
):
    if token_data.user_type not in [UserType.STUDENT, UserType.STAFF, UserType.ADMIN]:
        raise AuthorisationFailed()
    
    # make sure the external profile exists
    external_profile = await service.get_external_profile_by_id(
        external_profile_id=external_profile_id, session=session)

    if token_data.user_type == UserType.STUDENT:
        # check if the external profile belongs to the student
        if external_profile.student_id != token_data.related_entity_id:
            raise AuthorisationFailed()
        
    return external_profile

async def verify_activity_access(
    activity_id: int,
    token_data: TokenData = Depends(get_token_data),
    session: AsyncSession = Depends(get_session)
):
    if token_data.user_type not in [UserType.STUDENT, UserType.STAFF, UserType.ADMIN]:
        raise AuthorisationFailed()
    
    # make sure the activity exists
    activity = await service.get_student_activity_by_id(activity_id=activity_id, session=session)
    if activity is None:
        raise ActivityNotFound()
    
    # if student -- check if the activity belongs to the student
    if token_data.user_type == UserType.STUDENT:
        if activity.student_id != token_data.related_entity_id:
            raise AuthorisationFailed()
    
    return activity

def student_activity_common_params(
    student_id: Union[ConstrainedId, None] = None,
    activity_type: Union[ActivityType, None] = None
):
    return {
        "student_id": student_id,
        "activity_type": activity_type
    }

StudentActivityCommonsDep = Annotated[dict, Depends(student_activity_common_params)]
    
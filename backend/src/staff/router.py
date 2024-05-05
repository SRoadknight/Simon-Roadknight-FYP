from fastapi import APIRouter, Depends, Query
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user
from src.auth.models import TokenData
from src.database import get_session
from src.models import ConstrainedId
from sqlmodel.ext.asyncio.session import AsyncSession
from src.staff import service
from src.staff.models import CareersStaffUpdate, CareersStaffReadWithUser
from src.interactions.models import StaffInteractionUpdate, InteractionCreate, InteractionReadWithStudent
from src.interactions.dependencies import verify_interaction_modify_access
from src.interactions.service import update_interaction as staff_update_interaction
from src.interactions.service import create_interaction as staff_create_interaction
from src.appointments.dependencies import AppointmentCommonsDep
from src.interactions.dependencies import InteractionCommonsDep
from src.students.service import get_student_by_id
from src.students.exceptions import StudentNotFound


router = APIRouter(dependencies=[Depends(get_current_active_user)]) 


# Get all staff members
@router.get("", response_model=list[CareersStaffReadWithUser])
async def read_staff_members(
    session: AsyncSession = Depends(get_session)
):
    staff = await service.get_staff(session=session)
    return staff

# Get own staff profile
@router.get("/me", response_model=CareersStaffReadWithUser)
async def read_own_staff_profile(
    token_data: TokenData = Depends(get_current_active_staff_user),
    session: AsyncSession = Depends(get_session)
):
    staff = await service.get_staff_with_user(
        staff_id=token_data.related_entity_id,
        session=session
    )
    return staff


# Update a staff members profile
@router.patch("/me", response_model=CareersStaffReadWithUser)
async def update_own_staff_profile(
    *,
    token_data: TokenData = Depends(get_current_active_staff_user),
    staff_update: CareersStaffUpdate,
    session: AsyncSession = Depends(get_session)
):
    staff = await service.update_staff(
        staff_id=token_data.related_entity_id,
        staff_update=staff_update,
        session=session
    )
    return staff

# Career staff appointments / view their appointments
@router.get("/me/appointments")
async def read_staff_appointments(
    *,
    commons: AppointmentCommonsDep ,
    token_data: TokenData = Depends(get_current_active_staff_user),
    session: AsyncSession = Depends(get_session)
):
    commons['staff_id'] = token_data.related_entity_id
    appointments = await service.get_staff_appointments(
        session=session,
        commons=commons
    )
    return appointments


# Career staff interactions / view their interactions
@router.get("/me/interactions", response_model=list[InteractionReadWithStudent])
async def read_staff_interactions(
    *,
    commons: InteractionCommonsDep,
    token_data: TokenData = Depends(get_current_active_staff_user),
    session: AsyncSession = Depends(get_session)
):
    commons['careers_staff_id'] = token_data.related_entity_id
    commons['read_student'] = True
    interactions = await service.get_staff_interactions(
        session=session,
        commons=commons
    )
    return interactions


# Career staff create a new interaction
@router.post("/me/interactions", response_model=InteractionReadWithStudent)
async def create_interaction(
    interaction: InteractionCreate,
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(get_current_active_staff_user)
):
    student = await get_student_by_id(session=session, student_id=interaction.student_id)
    if student is None:
        raise StudentNotFound()
    return await staff_create_interaction(session, interaction, staff_id=token_data.related_entity_id)


# Career staff update an interaction
@router.patch("/interactions/{interaction_id}")
async def update_interaction(
    interaction_id: int,
    interaction: StaffInteractionUpdate,
    _: TokenData = Depends(verify_interaction_modify_access),
    session: AsyncSession = Depends(get_session)
):
    
    interaction = await staff_update_interaction(
        interaction_id=interaction_id,
        interaction=interaction,
        session=session
    )
    return interaction


# Student gets career staff profile
@router.get("/{staff_id}", response_model=CareersStaffReadWithUser)
async def read_staff_profile(
    staff_id: ConstrainedId,
    session: AsyncSession = Depends(get_session)
):
    staff = await service.get_staff_with_user(
        staff_id=staff_id,
        session=session
    )
    return staff

# Student gets career staff appointments
@router.get("/{staff_id}/appointments")
async def read_staff_appointments(
    staff_id: ConstrainedId,
    commons: AppointmentCommonsDep,
    session: AsyncSession = Depends(get_session)
):
    commons['staff_id'] = staff_id
    appointments = await service.get_staff_appointments(
        session=session,
        commons=commons
    )
    return appointments
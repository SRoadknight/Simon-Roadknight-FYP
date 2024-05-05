from fastapi import APIRouter, Depends, Response, status, Query
from src.auth.models import User, TokenData
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user, get_token_data
from src.appointments.dependencies import AppointmentCommonsDep, verify_can_manage_own_appointments
from src.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.appointments import service
from src.appointments.models import (
    AppointmenReadWithDetails,
    AppointmentCreate,
    AppointmentUpdate,
)

router = APIRouter(dependencies=[Depends(get_current_active_user)])


# Get all available appointments
@router.get("")
async def read_appointments(
    *,
    commons: AppointmentCommonsDep,
    session: AsyncSession = Depends(get_session)
):
    appointments = await service.get_appointments(session=session, **commons)
    return appointments



# Read a single appointment
@router.get("/{appointment_id}", response_model=AppointmenReadWithDetails)
async def read_appointment(
    appointment_id: int, 
    session: AsyncSession = Depends(get_session)
    ):
    appointment = await service.get_appointment_with_details(
        appointment_id=appointment_id, 
        session=session)
    return appointment

    

# Create a new appointment
@router.post("")
async def create_appointment(
    appointment: AppointmentCreate,
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(get_token_data),
    current_user: User = Depends(get_current_active_staff_user),
    ):
    return await service.create_appointment(
        appointment=appointment, 
        staff_id=token_data.related_entity_id,
        session=session)

# Update an appointment
@router.patch("/{appointment_id}")
async def update_appointment(
    *,
    _current_user: User = Depends(get_current_active_staff_user),
    appointment_id: int,
    appointment: AppointmentUpdate,
    token_data: TokenData = Depends(get_token_data),
    session: AsyncSession = Depends(get_session)
    ):
    return await service.update_appointment(
        appointment_id=appointment_id, 
        appointment=appointment, 
        staff_id=token_data.related_entity_id,
        session=session)

# Delete (cancel) an appointment
@router.patch("/{appointment_id}/cancel-appointment")
async def delete_appointment(
    *,
    _current_user: User = Depends(get_current_active_staff_user),
    appointment_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    return await service.cancel_appointment(appointment_id=appointment_id, session=session)


# Add a single skill to an appointment
@router.post("/{appointment_id}/skills/{skill_id}")
async def add_skill_to_appointment(
    appointment_id: int, 
    skill_id: int, 
    session: AsyncSession = Depends(get_session),
    _current_user: User = Depends(get_current_active_staff_user)):
    return await service.add_skill_to_appointment(
        appointment_id=appointment_id, 
        skill_id=skill_id, 
        session=session)

# Remove a single skill from an appointment
@router.delete("/{appointment_id}/skills/{skill_id}")
async def remove_skill_from_appointment(
    appointment_id: int, 
    skill_id: int, 
    session: AsyncSession = Depends(get_session),
    _current_user: User = Depends(get_current_active_staff_user)):
    return await service.remove_skill_from_appointment(
        appointment_id=appointment_id, 
        skill_id=skill_id, 
        session=session)

# Get all skills associated with an appointment
@router.get("/{appointment_id}/skills")
async def get_appointment_skills(
    appointment_id: int, 
    session: AsyncSession = Depends(get_session)):
    return await service.get_appointment_skills(appointment_id=appointment_id, session=session)


# Book an appointment
@router.post("/{appointment_id}/book-appointment")
async def book_appointment(
    appointment_id: int,
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(verify_can_manage_own_appointments)
    ):
    return await service.book_appointment(
        appointment_id=appointment_id, 
        student_id=token_data.related_entity_id, 
        session=session)

# Cancel a booking for an appointment
@router.patch("/{appointment_id}/cancel-booking")
async def cancel_booking(
    appointment_id: int,
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(verify_can_manage_own_appointments)
    ):
    return await service.cancel_booking(
        appointment_id=appointment_id, 
        student_id=token_data.related_entity_id, 
        session=session)




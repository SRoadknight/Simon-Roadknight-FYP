from src.appointments import service
from src.appointments.exceptions import AppointmentNotFound, AuthorisationFailed
from src.auth.models import TokenData
from src.auth.dependencies import get_token_data
from src.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.models import ConstrainedId
from src.appointments.models import AppointmentStatus, AppointmentType
from typing import Union, Annotated




async def verify_staff_owns_appointment(
    *,
    token_data: TokenData = Depends(get_token_data),
    appointment_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    appointment = await service.get_appointment_by_id(appointment_id=appointment_id, session=session)
    if appointment is None:
        raise AppointmentNotFound()
    if appointment.staff_id != token_data.user_id:
        raise AuthorisationFailed()
    return appointment


async def verify_can_manage_own_appointments(
    *,
    token_data: TokenData = Depends(get_token_data),
    appointment_id: int,
    session: AsyncSession = Depends(get_session)
    ):
   if token_data.user_type != "student":
       raise AuthorisationFailed()
   return token_data

def appointment_common_params(
    student_id: Union[ConstrainedId, None] = None,
    staff_id: Union[ConstrainedId, None] = None,
    appointment_status: Union[AppointmentStatus, None] = None,
    appointment_type: Union[AppointmentType, None] = None,
    ):
    return {
        "student_id": student_id,
        "staff_id": staff_id,
        "appointment_status": appointment_status,
        "appointment_type": appointment_type,
    }

AppointmentCommonsDep = Annotated[dict, Depends(appointment_common_params)]
from datetime import date, time, timedelta, datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import  selectinload
from sqlalchemy import or_, and_
from typing import Union


from src.appointments.models import (
    Appointment,
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentSkillTag,
    AppointmentStatus,
    AppointmentBooking,
    AppointmentType
) 
from src.appointments.exceptions import (
    AppointmentNotFound, 
    AppointmentSlotNotAvailable,
    AppointmentAlreadyCancelled,
    SkillAlreadyAssignedToAppointment,
    SkillNotAssignedToAppointment,
    AppointmentSlotNotAvailable,
    StudentNotBookedForAppointment,
    AppointmentsOverlap
)
from src.models import ConstrainedId
from src.crud import (
    create_generic, 
    update_generic,
    add_skills_to_entity_on_create, 
    add_skill_to_entity, 
    remove_skill_from_entity
)



async def get_appointments(
        session: AsyncSession,
        appointment_type: Union[AppointmentType, None] = None,
        appointment_status: Union[AppointmentStatus, None] = None,
        student_id: Union[ConstrainedId, None] = None,
        staff_id: Union[ConstrainedId, None] = None
    ):
    
    query = select(Appointment).options(selectinload(Appointment.skills).joinedload(AppointmentSkillTag.skill))

    conditions = []


    if appointment_type:
        conditions.append(Appointment.type == appointment_type)
    if appointment_status:
        conditions.append(Appointment.status == appointment_status)
    if student_id:
        conditions.append(Appointment.students.any(AppointmentBooking.student_id == student_id))
    if staff_id:
        conditions.append(Appointment.staff_id == staff_id)

    query = query.where(*conditions)

    result = await session.exec(query)
    appointments = result.all()
    return appointments


async def get_appointment_by_id(appointment_id: int, session: AsyncSession):
    result = await session.exec(select(Appointment).where(Appointment.id == appointment_id))
    appointment = result.first()
    return appointment


async def get_appointment_with_details(
        *,
        appointment_id: int, 
        session: AsyncSession):
    result = await session.exec(
        select(Appointment)
        .where(Appointment.id == appointment_id)
        .options(selectinload(Appointment.skills).joinedload(AppointmentSkillTag.skill)))
    appointment = result.first()
    if appointment is None:
        raise AppointmentNotFound()
    return appointment
    

async def check_appointment_slot_availability(
    *,
    appointment_id: Union[int, None] = None,
    app_start_time: Union[datetime, None] = None,
    length_minutes: Union[int, None] = None,
    student: bool = False,
    entity_id: ConstrainedId,
    session: AsyncSession):

    if appointment_id is not None:
        result = await get_appointment_by_id(appointment_id=appointment_id, session=session)
        if result is None:
            raise AppointmentNotFound()
        

    if app_start_time is None:
        app_start_time = result.app_start_time
    if length_minutes is None:
        length_minutes = result.app_end_time - result.app_start_time
        length_minutes = length_minutes.total_seconds() // 60

    query = select(Appointment).where(
            (Appointment.id != appointment_id) if appointment_id else True,
            Appointment.staff_id == entity_id if not student else True,
            Appointment.status.in_([AppointmentStatus.available, AppointmentStatus.booked]),
            or_(
                and_(
                    Appointment.app_start_time <= app_start_time,
                    Appointment.app_end_time >= app_start_time
                ),
                and_(
                    Appointment.app_start_time <= app_start_time + timedelta(minutes=length_minutes),
                    Appointment.app_end_time >= app_start_time + timedelta(minutes=length_minutes)
                ),
                and_(
                    Appointment.app_start_time >= app_start_time,
                    Appointment.app_end_time <= app_start_time + timedelta(minutes=length_minutes   
                    )
                )
            )
        )
    if student:
        query = query.options(selectinload(Appointment.students)).where(AppointmentBooking.student_id == entity_id)

    result = await session.exec(query)
    overlapping_appointments = result.all()
    return len(overlapping_appointments) == 0

    


async def create_appointment(appointment: AppointmentCreate, staff_id: ConstrainedId, session: AsyncSession):
    if not await check_appointment_slot_availability(
        app_start_time=appointment.app_start_time,
        length_minutes=appointment.length_minutes,
        entity_id=staff_id,
        session=session
    ):
        raise AppointmentsOverlap()
    
    end_time = appointment.app_start_time + timedelta(minutes=appointment.length_minutes)
    db_appointment = await create_generic(
        model_class=Appointment, 
        create_data=appointment, 
        session=session,
        extra_data={"staff_id": staff_id, "app_end_time": end_time})
    await add_skills_to_entity_on_create(
        entity_id=db_appointment.id,
        entity_model=AppointmentSkillTag,
        skill_data=appointment.skill_data,
        foreign_key="appointment_id",
        session=session
    )
    await session.commit()
    await session.refresh(db_appointment)
    return db_appointment


async def update_appointment(
        appointment_id: int, 
        appointment: AppointmentUpdate, 
        staff_id: ConstrainedId,
        session: AsyncSession):
    if appointment.app_start_time is not None or appointment.length is not None:
        if not await check_appointment_slot_availability(
            appointment_id=appointment_id,
            app_start_time=appointment.app_start_time or None,
            length_minutes=appointment.length_minutes or None,
            entity_id=staff_id,
            session=session
        ):
            raise AppointmentsOverlap()
        else:
            end_time = appointment.app_start_time + timedelta(minutes=appointment.length_minutes)
            appointment.app_end_time = end_time

    return await update_generic(
        model_id=appointment_id,
        update_data=appointment,
        model_getter=get_appointment_by_id,
        session=session
    )

async def cancel_appointment(appointment_id: int, session: AsyncSession):
    appointment = await get_appointment_by_id(appointment_id=appointment_id, session=session)
    if appointment is None:
        raise AppointmentNotFound()
    if appointment.status == "cancelled":
        raise AppointmentAlreadyCancelled()
    appointment.status = AppointmentStatus.cancelled
    await session.commit()
    return appointment


async def add_skill_to_appointment(appointment_id: int, skill_id: int, session: AsyncSession):
    appointment = await get_appointment_by_id(appointment_id=appointment_id, session=session)
    if appointment is None:
        raise AppointmentNotFound()
    return await add_skill_to_entity(
        skill_tag_base_model=AppointmentSkillTag,
        skill_tag_create_model=AppointmentSkillTag,
        entity_id=appointment_id,
        skill_id=skill_id,
        foreign_key="appointment_id",
        exception=SkillAlreadyAssignedToAppointment,
        session=session
    )

async def remove_skill_from_appointment(appointment_id: int, skill_id: int, session: AsyncSession):
    appointment = await get_appointment_by_id(appointment_id=appointment_id, session=session)
    if appointment is None:
        raise AppointmentNotFound()
    return await remove_skill_from_entity(
        entity_id=appointment_id,
        skill_id=skill_id,
        skill_tag_base_model=AppointmentSkillTag,
        foreign_key="appointment_id",
        exception=SkillNotAssignedToAppointment,
        session=session
    )

async def get_appointment_skills(appointment_id: int, session: AsyncSession):
    appointment = await get_appointment_by_id(appointment_id=appointment_id, session=session)
    if appointment is None:
        raise AppointmentNotFound()
    return appointment.skills


async def check_student_booking(appointment_id: int, student_id: ConstrainedId, session: AsyncSession):
    result = await session.exec(
        select(AppointmentBooking).where(
            AppointmentBooking.appointment_id == appointment_id,
            AppointmentBooking.student_id == student_id
        )
    )
    appointment = result.first()
    return appointment is not None

async def book_appointment(appointment_id: int, student_id: ConstrainedId, session: AsyncSession):
    appointment = await get_appointment_by_id(appointment_id=appointment_id, session=session)
    if appointment is None:
        raise AppointmentNotFound()
    if appointment.status != "available":
        raise AppointmentSlotNotAvailable()
    
    slot_available = await check_appointment_slot_availability(
        appointment_id=appointment_id,
        student=True,
        entity_id=student_id,
        session=session
    )
    if not slot_available:
        raise AppointmentsOverlap()
    
    appointment.status = AppointmentStatus.booked
    appointment_booking_data = {"appointment_id": appointment_id, "student_id": student_id}
    db_appointment_booking = AppointmentBooking.model_validate(appointment_booking_data)
    session.add(db_appointment_booking)
    await session.commit()
    return appointment

async def cancel_booking(appointment_id: int, student_id: ConstrainedId, session: AsyncSession):
    appointment = await get_appointment_by_id(appointment_id=appointment_id, session=session)
    if appointment is None:
        raise AppointmentNotFound()
    if appointment.status != "booked":
        raise AppointmentNotFound()
    student_booked = await check_student_booking(appointment_id=appointment_id, student_id=student_id, session=session)
    if not student_booked:
        raise StudentNotBookedForAppointment()
    
        
    appointment.status = AppointmentStatus.available
    result = await session.exec(
        select(AppointmentBooking).where(
            AppointmentBooking.appointment_id == appointment_id,
            AppointmentBooking.student_id == student_id
        )
    )
    appointment_booking = result.first()
    await session.delete(appointment_booking)
    await session.commit()
    return appointment

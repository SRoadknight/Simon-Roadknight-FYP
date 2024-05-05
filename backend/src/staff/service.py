from src.models import ConstrainedId
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.crud import update_generic
from src.staff.models import CareersStaff, CareersStaffUpdate
from src.applications.dependencies import ApplicationCommonsDep
from src.appointments.service import get_appointments
from sqlalchemy.orm import joinedload
from src.interactions.service import get_interactions

async def get_staff(session: AsyncSession):
    result = await session.exec(
        select(CareersStaff)
        .options(joinedload(CareersStaff.user)))
    staff = result.all()
    return staff

async def get_staff_by_id(staff_id: ConstrainedId, session: AsyncSession):
    result = await session.exec(select(CareersStaff).where(CareersStaff.id == staff_id))
    staff = result.first()
    return staff

async def get_staff_with_user(staff_id: ConstrainedId, session: AsyncSession):
    result = await session.exec(
        select(CareersStaff)
        .options(joinedload(CareersStaff.user))
        .where(CareersStaff.id == staff_id)
    )
    staff = result.first()
    return staff

async def update_staff(
        staff_id: ConstrainedId, 
        staff_update: CareersStaffUpdate, 
        session: AsyncSession
        ):
    staff = await update_generic(
        model_id=staff_id,
        update_data=staff_update,
        model_getter=get_staff_by_id,
        session=session
    )
    await session.commit()
    return await get_staff_with_user(staff_id, session)


async def get_staff_appointments(
        session: AsyncSession,
        commons: ApplicationCommonsDep
    ):
    appointments = await get_appointments(session=session, **commons)
    return appointments

async def get_staff_interactions(
        session: AsyncSession,
        commons: ApplicationCommonsDep
    ):
    interactions = await get_interactions(session=session, **commons)
    return interactions







from sqlmodel import select
from typing import Union, TYPE_CHECKING
from sqlmodel.ext.asyncio.session import AsyncSession
from src.crud import create_generic, update_generic
from src.interactions.models import Interaction, InteractionCreate, StaffInteractionUpdate, StudentInteractionUpdate
from sqlalchemy.orm import selectinload
from src.staff.models import CareersStaff
from src.students.models import Student
from src.auth.models import User

if TYPE_CHECKING:
    from src.students.service import get_student_by_id



async def get_interactions(
        session: AsyncSession, 
        student_id: Union[int, None] = None,
        careers_staff_id: Union[int, None] = None,
        type: Union[int, None] = None,
        read_staff: bool = False,
        read_student: bool = False,
        outstanding: bool = False
    ):
    
    if read_staff and read_student:
        query = select(Interaction).options(selectinload(Interaction.careers_staff).selectinload(CareersStaff.user)).options(selectinload(Interaction.student).selectinload(Student.user))
    elif read_staff:
        query = select(Interaction).options(selectinload(Interaction.careers_staff).selectinload(CareersStaff.user))
    elif read_student:
        query = select(Interaction).options(selectinload(Interaction.student).selectinload(Student.user))
    else:
        query = select(Interaction)


    conditions = []

    if type:
        conditions.append(Interaction.type == type)
    if student_id:
        conditions.append(Interaction.student_id == student_id)
    if careers_staff_id:
        conditions.append(Interaction.careers_staff_id == careers_staff_id)
    if outstanding:
        conditions.append(Interaction.updated_by_student == False)

    query = query.where(*conditions)

    result = await session.exec(query)
    interactions = result.all()
    return interactions


async def get_interaction_by_id(interaction_id: int, session: AsyncSession, student_read: bool = False):
    if student_read:
        query = select(Interaction).options(selectinload(Interaction.careers_staff).selectinload(CareersStaff.user))
    else:
        query = select(Interaction).options(selectinload(Interaction.student).selectinload(Student.user))

    query = query.where(Interaction.id == interaction_id)
    result = await session.exec(query)
    interaction = result.first()
    return interaction

async def create_interaction(session: AsyncSession, interaction: InteractionCreate, staff_id):
    interaction = await create_generic(
        model_class=Interaction,
        create_data=interaction,
        session=session,
        extra_data={"careers_staff_id": staff_id}
    )

    return await get_interaction_by_id(interaction.id, session)

async def update_interaction(
        interaction_id: int, 
        interaction: Union[StaffInteractionUpdate, StudentInteractionUpdate], 
        session: AsyncSession,
        student: bool = False
        ):
    student_read = False
    db_interaction = await update_generic(
        model_id=interaction_id,
        update_data=interaction,
        model_getter=get_interaction_by_id,
        session=session
    )
    if student:
        db_interaction.updated_by_student = True
        session.add(db_interaction)
        student_read = True
    await session.commit()
    await session.refresh(db_interaction)
    return await get_interaction_by_id(interaction_id, session, student_read=student_read)



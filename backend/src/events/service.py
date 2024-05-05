from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Union
from sqlmodel import select
from sqlalchemy.orm import selectinload
from src.events.models import (
    Event, 
    EventSkillTag, 
    EventCreate, 
    EventUpdate,
    EventSkillTagCreate,
    EventRegistration,
    EventType,
    EventStatus
)
from src.events.exceptions import (
    EventNotFound, 
    SkillNotAssignedToEvent,
    StudentAlreadyRegisteredToEvent,
    StudentNotRegisteredToEvent,
)


from src.crud import (
    create_generic, 
    update_generic,
    add_skills_to_entity_on_create, 
    add_skill_to_entity,
    remove_skill_from_entity,
    validate_skill_tags
)

from src.models import ConstrainedId
from src.students.models import Student
from src.skill_tags.service import get_skill_by_id
from src.skill_tags.exceptions import SkillTagNotFound

async def get_events(
        session: AsyncSession,
        event_type:  Union[EventType, None] = None,
        event_status: Union[EventStatus, None] = None,
        student_id: Union[ConstrainedId, None] = None
):
    query = select(Event).options(selectinload(Event.skills).joinedload(EventSkillTag.skill))
    
    conditions = []

    if event_type:
        conditions.append(Event.event_type == event_type)
    if event_status:
        conditions.append(Event.status == event_status)
    if student_id:
        conditions.append(Event.students.any(EventRegistration.student_id == student_id))
    if not event_status:
        conditions.append(Event.status == "upcoming")

    query = query.where(*conditions)

    result = await session.exec(query)
    events = result.all()
    return events

async def get_event_by_id(event_id: int, session: AsyncSession):
    result = await session.exec(select(Event).where(Event.id == event_id)
            .options(selectinload(Event.skills).joinedload(EventSkillTag.skill)))
    event = result.first()
    if not event:
        raise EventNotFound()
    return event



async def create_event(event: EventCreate, session: AsyncSession):

    skill_data = event.skill_data
    await validate_skill_tags(skill_data, session=session)
    

    db_event = await create_generic(model_class=Event, create_data=event, session=session)
    await add_skills_to_entity_on_create(
        entity_id=db_event.id, 
        entity_model=EventSkillTag, 
        skill_data=skill_data, 
        foreign_key="event_id",
        session=session
    )

    await session.commit()
    await session.refresh(db_event)
    return db_event

    
    


# update an event
async def update_event(event_id: int, event: EventUpdate, session: AsyncSession):
    return await  update_generic(
        model_id=event_id,
        update_data=event,
        model_getter=get_event_by_id,
        session=session
    )
      

# soft delete event (cancel)
async def soft_delete_event(event_id: int, session: AsyncSession):
    event = await get_event_by_id(event_id=event_id, session=session)
    event.status = "cancelled"
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event

# add a single skill to an event
async def add_skill_to_event(
        *,
        event_id: int, 
        skill_name: Union[str, None] = None,
        skill_id: Union[int, None] = None, 
        session: AsyncSession):
    event = await get_event_by_id(event_id=event_id, session=session)
    if event is None:
        raise EventNotFound()
    return await add_skill_to_entity(
        skill_tag_base_model=EventSkillTag,
        skill_tag_create_model=EventSkillTagCreate,
        entity_id=event_id,
        skill_name=skill_name,
        skill_id=skill_id,
        foreign_key="event_id",
        session=session
    )

# remove a single skill from an event
async def remove_skill_from_event(event_id: int, skill_id: int, session: AsyncSession):
    event = await get_event_by_id(event_id=event_id, session=session)
    if event is None:
        raise EventNotFound()
    return await remove_skill_from_entity(
        entity_id=event_id,
        skill_id=skill_id,
        skill_tag_base_model=EventSkillTag,
        foreign_key="event_id",
        exception=SkillNotAssignedToEvent,
        session=session
    )
    

# check if studen is registered for an event
async def check_student_registration(event_id: int, student_id: ConstrainedId, session: AsyncSession):
    result = await session.exec(
        select(EventRegistration).where(EventRegistration.event_id == event_id, EventRegistration.student_id == student_id)
    )
    registration = result.first()
    return registration

# student register for an event
async def register_for_event(event_id: int, student_id: ConstrainedId, session: AsyncSession):
    event = await get_event_by_id(event_id=event_id, session=session)
    if event is None:
        raise EventNotFound()
    if await check_student_registration(event_id=event_id, student_id=student_id, session=session):
        raise StudentAlreadyRegisteredToEvent()
    event_registration_data = {"student_id": student_id, "event_id": event_id}
    db_event_registration = EventRegistration.model_validate(event_registration_data)
    session.add(db_event_registration)
    await session.commit()

# student unregisters for an event
    event = await get_event_by_id(event_id=event_id, session=session)
    if event is None:
        raise EventNotFound()
async def unregister_from_event(event_id: int, student_id: ConstrainedId, session: AsyncSession):
    event_registration = await check_student_registration(event_id=event_id, student_id=student_id, session=session)
    if not event_registration:
        raise StudentNotRegisteredToEvent()
    await session.delete(event_registration)
    await session.commit()


async def get_event_registrations(event_id: int, session: AsyncSession):
    result = await session.exec(
        select(EventRegistration)
        .options(selectinload(EventRegistration.student).joinedload(Student.user))
        .where(EventRegistration.event_id == event_id)
    )
    registrations = result.all()
    return registrations
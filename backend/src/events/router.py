from fastapi import APIRouter, Depends, Response, status, Query
from src.auth.models import User, TokenData
from src.auth.dependencies import get_current_active_user, get_current_active_staff_user
from src.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.events import service
from src.events.models import (
    EventCreate,
    EventRead,
    EventUpdate,
    EventSkillTagRead,
    EventReadWithSkills,
    EventRegistrationReadWithStudent

)
from src.events.dependencies import (
    verify_can_manage_own_events,
    EventCommonsDep
)
from src.students.models import StudentReadWithUser
from typing import Union


router = APIRouter(dependencies=[Depends(get_current_active_user)])



# Get filtered events
@router.get("", response_model=list[EventReadWithSkills])
async def read_events(
    commons: EventCommonsDep,
    session: AsyncSession = Depends(get_session)
):
    event = await service.get_events(session=session, **commons)
    return event



# Read a single event
@router.get("/{event_id}", response_model=EventRead)
async def read_event(
    event_id: int, 
    session: AsyncSession = Depends(get_session)
    ):
    event = await service.get_event_by_id(event_id=event_id, session=session)
    return event

# Create a new event
@router.post("")
async def create_event(
    event: EventCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_staff_user)
    ):
    return await service.create_event(event=event, session=session)

    
# Update an event
@router.patch("/{event_id}", response_model=EventRead)
async def update_event(
    *,
    _current_user: User = Depends(get_current_active_staff_user),
    event_id: int,
    event: EventUpdate,
    session: AsyncSession = Depends(get_session)
    ):
    return await service.update_event(
        event_id=event_id, 
        event=event, 
        session=session)

# See who is registered for an event
@router.get("/{event_id}/registrations", response_model=list[EventRegistrationReadWithStudent])
async def read_event_registrations(
    event_id: int,
    session: AsyncSession = Depends(get_session),
    _current_user: User = Depends(get_current_active_staff_user)
    ):
    return await service.get_event_registrations(event_id=event_id, session=session)



# Delete an event (soft delete making it inactive)
@router.patch("/{event_id}/soft-delete", response_model=EventRead)
async def delete_event(
    *,
    current_user: User = Depends(get_current_active_staff_user),
    event_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    return await service.soft_delete_event(event_id, session=session)

# Add a single skill to an event
@router.post("/{event_id}/skills")
async def add_skill_to_event(
    event_id: int, 
    skill_name: Union[str, None] = Query(None),
    skill_id: Union[int, None] = Query(None),
    session: AsyncSession = Depends(get_session),
    _current_user: User = Depends(get_current_active_staff_user)):
    
    return await service.add_skill_to_event(
        event_id=event_id, 
        skill_name=skill_name,
        skill_id=skill_id, 
        session=session)
    


# remove a single skill from an event
@router.delete("/{event_id}/skills/{skill_id}")
async def remove_skill_from_event(
    event_id: int, 
    skill_id: int, 
    session: AsyncSession = Depends(get_session),
    _current_user: User = Depends(get_current_active_staff_user)):
    return await service.remove_skill_from_event(
        event_id=event_id, 
        skill_id=skill_id, 
        session=session)

# Get all skills for an event
@router.get("/{event_id}/skills", response_model=list[EventSkillTagRead])
async def read_event_skills(
    event_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    event = await service.get_event_by_id(event_id, session=session)
    return event.skills



# Register for event 
@router.post("/{event_id}/register")
async def register_for_event(
    event_id: int,
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(verify_can_manage_own_events)
    ):
    await service.register_for_event(
        event_id=event_id, 
        session=session, 
        student_id=token_data.related_entity_id)
    return Response(status_code=status.HTTP_200_OK)


# Unregister from event
@router.delete("/{event_id}/unregister", response_model=EventRead)
async def unregister_from_event(
    *,
    event_id: int,
    session: AsyncSession = Depends(get_session),
    token_data: TokenData = Depends(verify_can_manage_own_events)
    ):
    await service.unregister_from_event(
        event_id=event_id, 
        session=session, 
        student_id=token_data.related_entity_id)
    return Response(status_code=status.HTTP_200_OK)


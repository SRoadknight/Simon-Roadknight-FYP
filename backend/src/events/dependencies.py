from src.events.exceptions import EventNotFound, EventNotActive
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from fastapi import Depends
from src.events import service
from src.auth.models import TokenData 
from src.auth.dependencies import get_token_data
from src.auth.exceptions import AuthorisationFailed
from src.events.models import EventStatus, EventType
from typing import Union, Annotated
from src.models import ConstrainedId


async def valid_active_event(
    event_id: int, 
    session: AsyncSession = Depends(get_session)
    ):
    event = await service.get_event_by_id(event_id=event_id, session=session)
    if event is None:
        raise EventNotFound()
    if event.status != "active":
        raise EventNotActive()
    return event
    
async def valid_event(
    event_id: int, 
    session: AsyncSession = Depends(get_session)
    ):
    event = await service.get_event_by_id(event_id=event_id, session=session)
    return event

async def verify_can_manage_own_events(
    token_data: TokenData = Depends(get_token_data)
    ):
    if token_data.user_type == "student":
        return token_data
    raise AuthorisationFailed()

def event_common_params(
        event_type: Union[EventType, None] = None,
        event_status: Union[EventStatus, None] = None,
        student_id: Union[ConstrainedId, None] = None
):
    return {
        "event_type": event_type,
        "event_status": event_status,
        "student_id": student_id
    }

EventCommonsDep = Annotated[dict, Depends(event_common_params)]
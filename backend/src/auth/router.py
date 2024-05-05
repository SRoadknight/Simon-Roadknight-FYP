from datetime import timedelta
from typing import Annotated, Union

from src.database import get_session


from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.jwt import create_access_token
from src.auth.service import authenticate_user
from src.auth.dependencies import get_current_active_user
from src.auth.config import auth_config
from src.auth.models import Token
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.models import User, UserRead

from src.auth import service

router = APIRouter()


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(username=form_data.username, password=form_data.password, session=session)
    related_entity_id = await service.get_entity_id_by_user_id(session=session, user=user)
    access_token_expires = timedelta(minutes=auth_config.JWT_EXP)
    access_token = create_access_token(
        data={
            "sub": user.email_address,
            "user_id": user.id,
            "user_type": user.user_type, 
            "disabled": user.disabled,
            "related_entity_id": related_entity_id}, 
            expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)], session: AsyncSession = Depends(get_session)
):
    return current_user
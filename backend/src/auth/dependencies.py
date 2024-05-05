from fastapi import Depends
from jose import JWTError, jwt
from src.auth.config import auth_config
from src.auth.models import TokenData, User
from src.database import get_session
from typing import Annotated
from src.auth import service
from src.auth.jwt import oauth2_scheme
from src.auth.exceptions import (
    InvalidCredentials, 
    InactiveUser,
    NotAuthenticated,
    AuthorisationFailed
)
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidCredentials()
        token_data = TokenData(sub=username)
    except JWTError:
        raise InvalidCredentials()
    user = await service.get_user_by_email(email=token_data.sub, session=session)
    if user is None:
        raise NotAuthenticated()
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise InactiveUser()
    return current_user


async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidCredentials()
        token_data = TokenData(**payload)
    except JWTError:
        raise InvalidCredentials()
    return token_data


async def get_current_active_staff_user(current_user: Annotated[User, Depends(get_current_active_user)], token_data: Annotated[TokenData, Depends(get_token_data)]):
    if current_user.user_type in ["staff", "admin"]:
        return token_data
    raise AuthorisationFailed()


async def get_current_active_student_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    token_data: Annotated[TokenData, Depends(get_token_data)]):
    if current_user.user_type == "student":
        return token_data
    raise AuthorisationFailed()

async def get_current_active_company_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    token_data: Annotated[TokenData, Depends(get_token_data)]):
    if current_user.user_type == "company":
        return token_data
    raise AuthorisationFailed()

from typing import Annotated, Union, Type
from sqlmodel import select
from src.auth.security import verify_password
from src.auth.models import User, UserType
from src.auth.exceptions import InvalidCredentials, UserAlreadyDisabled, UserNotDisabled
from sqlmodel.ext.asyncio.session import AsyncSession
from src.companies.models import CompanyUserCreate
from src.staff.models import CareersStaffUserCreate
from src.students.models import StudentUserCreate
from src.auth.utils import model_mapping
from sqlmodel import select, SQLModel
from src.exceptions import NotFound



async def get_entity_id_by_user_id(session: AsyncSession, user: User):
    model = model_mapping.get(user.user_type)
    if model is None:
         raise InvalidCredentials()
    
    result = await session.exec(select(model).where(model.user_id == user.id))
    entity = result.first()
    return entity.id


async def get_user_by_entity_id(
    entity_id: int, session: AsyncSession, entity_model: Type[SQLModel], exception: NotFound):
    result = await session.exec(
        select(User).join(entity_model).where(entity_model.id == entity_id)
    )
    user = result.first()
    if not user:
        raise exception
    return user


     

async def get_user_by_email(email: str, session: AsyncSession):
    # get user by email address
    email = email.lower()
    result = await session.exec(select(User).where(User.email_address == email))
    user = result.first()
    return user

async def get_user_by_id(user_id: int, session: AsyncSession):
    result = await session.exec(select(User).where(User.id == user_id))
    user = result.first()
    return user
    
            
async def authenticate_user(username: id, password: str, session: AsyncSession) -> Union[User, None]:
    user = await get_user_by_email(username, session)
    if user is None:
        raise InvalidCredentials()
    if not verify_password(password, user.hashed_password):
       raise InvalidCredentials() 
    return user

# create company user
async def create_company_user(company_user: CompanyUserCreate, session: AsyncSession):
    user_data = {"user_type": UserType.COMPANY, "email_address": company_user.email_address}
    db_user = User.model_validate(user_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

# create_user 
async def create_user(
    user: Union[CareersStaffUserCreate, StudentUserCreate, CompanyUserCreate], 
    session: AsyncSession):
    user_data_extra = {"user_type": 
                    UserType.STAFF if isinstance(user, CareersStaffUserCreate) 
                    else UserType.STUDENT if isinstance(user, StudentUserCreate) 
                    else UserType.COMPANY}
    db_user = User.model_validate(user.model_dump(exclude="id"), update=user_data_extra)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user



# disable user account
async def disable_user_account(session: AsyncSession, user: User):
    if user.disabled:
        raise UserAlreadyDisabled()
    user.disabled = True
    await session.commit()
    return user

# enable user account
async def enable_user_account(session: AsyncSession, user: User):
    if not user.disabled:
        raise UserNotDisabled()
    user.disabled = False
    await session.commit()
    return user




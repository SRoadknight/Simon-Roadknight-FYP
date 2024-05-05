from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from fastapi import Depends
from src.companies.exceptions import CompanyNotFound, InvalidCompanyName
from src.companies import service
from src.models import ConstrainedId
from src.companies.models import CompanyUserCreate, CompanyUpdate

async def get_company_by_id(company_id: ConstrainedId, session: AsyncSession = Depends(get_session)):
    company = await service.get_company_by_id(session=session, company_id=company_id)
    if not company:
        raise CompanyNotFound()
    return company

async def validate_company_user_create(company_user: CompanyUserCreate, session: AsyncSession = Depends(get_session)):
    if company_user.name == "":
        raise InvalidCompanyName()
    await service.check_company_exists(session=session, company_id=company_user.id, company_name=company_user.name, user_email=company_user.email_address)
    return company_user

async def valid_company_update(company_update: CompanyUpdate, session: AsyncSession = Depends(get_session)):
    if company_update.name == "":
        raise InvalidCompanyName()
    await service.check_company_exists(session=session, company_name=company_update.name)
        
    return company_update
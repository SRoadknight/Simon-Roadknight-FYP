from src.exceptions import BadRequest
from src.companies.constants import ErrorCode

class CompanyAlreadyRegistered(BadRequest):
    DETAIL = ErrorCode.COMPANY_ALREADY_REGISTERED

class CompanyNotFound(BadRequest):
    DETAIL = ErrorCode.COMPANY_NOT_FOUND

class InvalidCompanyName(BadRequest):
    DETAIL = ErrorCode.INVALID_COMPANY_NAME
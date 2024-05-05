from src.auth.constants import ErrorCode 
from src.exceptions import NotAuthenticated, BadRequest

class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS

class AuthorisationFailed(NotAuthenticated):
    DETAIL = ErrorCode.AUTHORISATION_FAILED

class InactiveUser(BadRequest):
    DETAIL = ErrorCode.INACTIVE_USER

class UserAlreadyDisabled(BadRequest):
    DETAIL = ErrorCode.USER_ALREADY_DISABLED

class UserNotDisabled(BadRequest):
    DETAIL = ErrorCode.USER_NOT_DISABLED
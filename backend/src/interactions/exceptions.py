from src.exceptions import NotFound, PermissionDenied
from src.interactions.constants import ErrorCode

class InteractionNotFound(NotFound):
    DETAIL = ErrorCode.INTERACTION_NOT_FOUND

class InteractionNotVisible(PermissionDenied):
    DETAIL = ErrorCode.INTERACTION_NOT_VISIBLE
from src.exceptions import BadRequest, NotFound, PermissionDenied
from src.groups.constants import ErrorCode

class GroupNotFound(NotFound):
    DETAIL = ErrorCode.GROUP_NOT_FOUND

class StudentAlreadyInGroup(BadRequest):
    DETAIL = ErrorCode.STUDENT_ALREADY_IN_GROUP

class StudentNotInGroup(BadRequest):
    DETAIL = ErrorCode.STUDENT_NOT_IN_GROUP

class GroupNameAlreadyExists(BadRequest):
    DETAIL = ErrorCode.GROUP_NAME_ALREADY_EXISTS
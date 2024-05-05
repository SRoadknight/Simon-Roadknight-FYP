from src.events.constants import ErrorCode
from src.exceptions import BadRequest, PermissionDenied, NotFound

class EventNotFound(NotFound):
    DETAIL = ErrorCode.EVENT_NOT_FOUND

class EventNameEmpty(BadRequest):
    DETAIL = ErrorCode.EVENT_NAME_EMPTY

class EventTypeAlreadyExists(BadRequest):
    DETAIL = ErrorCode.EVENT_TYPE_ALREADY_EXISTS

class EventTypeNotFound(NotFound):
    DETAIL = ErrorCode.EVENT_TYPE_NOT_FOUND

class EventNotActive(BadRequest):
    DETAIL = ErrorCode.EVENT_NOT_ACTIVE

class SkillAlreadyAssignedToEvent(BadRequest):
    DETAIL = ErrorCode.SKILL_TAG_ALREADY_ASSIGNED

class SkillTagAlreadyAssigned(BadRequest):
    DETAIL = ErrorCode.SKILL_TAG_ALREADY_ASSIGNED

class SkillNotAssignedToEvent(BadRequest):
    DETAIL = ErrorCode.SKILL_NOT_ASSIGNED_TO_EVENT

class StudentAlreadyRegisteredToEvent(BadRequest):
    DETAIL = ErrorCode.STUDENT_ALREADY_REGISTERED_TO_EVENT

class StudentNotRegisteredToEvent(BadRequest):
    DETAIL = ErrorCode.STUDENT_NOT_REGISTERED_TO_EVENT

class UserNotAStudent(PermissionDenied):
    DETAIL = ErrorCode.USER_NOT_STUDENT

from src.exceptions import BadRequest, NotFound, PermissionDenied
from src.students.constants import ErrorCode

class StudentAlreadyRegistered(BadRequest):
    DETAIL = ErrorCode.STUDENT_ALREADY_REGISTERED

class StudentNotFound(NotFound):
    DETAIL = ErrorCode.STUDENT_NOT_FOUND

class StudentProfileNotVisible(PermissionDenied):
    DETAIL = ErrorCode.STUDENT_PROFILE_NOT_VISIBLE

class StudentDegreeAlreadyExists(BadRequest):
    DETAIL = ErrorCode.STUDENT_DEGREE_ALREADY_EXISTS

class StudentDegreeNotFound(NotFound):
    DETAIL = ErrorCode.STUDENT_DEGREE_NOT_FOUND

class ExternalProfileAlreadyExists(BadRequest):
    DETAIL = ErrorCode.EXTERNAL_PROFILE_ALREADY_EXISTS

class ExternalProfileNotFound(NotFound):
    DETAIL = ErrorCode.EXTERNAL_PROFILE_NOT_FOUND

class SkillTagAlreadyExists(BadRequest):
    DETAIL = ErrorCode.SKILL_TAG_ALREADY_EXISTS

class SkillTagNotAttached(BadRequest):
    DETAIL = ErrorCode.SKILL_TAG_NOT_ATTACHED

class ActivityNotFound(NotFound):
    DETAIL = ErrorCode.ACTIVITY_NOT_FOUND


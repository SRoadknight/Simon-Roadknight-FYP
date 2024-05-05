from src.exceptions import BadRequest, NotFound
from src.content.constants import ErrorCode

class ContentNotFound(NotFound):
    DETAIL = ErrorCode.CONTENT_NOT_FOUND


class SkillTagAlreadyAssigned(BadRequest):
    DETAIL = ErrorCode.SKILL_ALREADY_ASSIGNED_TO_CONTENT

class SkillTagNotAssigned(BadRequest):
    DETAIL = ErrorCode.SKILL_NOT_ASSIGNED_TO_CONTENT

class ContentNotInGroup(BadRequest):
    DETAIL = ErrorCode.CONTENT_NOT_IN_GROUP

class ContentAlreadyInGroup(BadRequest):
    DETAIL = ErrorCode.CONTENT_ALREADY_IN_GROUP
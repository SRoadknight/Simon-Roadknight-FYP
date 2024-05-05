from src.skill_tags.constants import ErrorCode
from src.exceptions import BadRequest

class SkillTagNotFound(BadRequest):
    DETAIL = ErrorCode.SKILL_TAG_NOT_FOUND

class SkillTagAlreadyExists(BadRequest):
    DETAIL = ErrorCode.SKILL_TAG_ALREADY_EXISTS

class SkillTagNameEmpty(BadRequest):
    DETAIL = ErrorCode.SKILL_TAG_NAME_EMPTY

class SkillTagInactive(BadRequest):
    DETAIL = ErrorCode.SKILL_TAG_INACTIVE

class SkillNameAndSkillIdBothProvided(BadRequest):
    DETAIL = ErrorCode.SKILL_NAME_AND_SKILL_ID_BOTH_PROVIDED 

class SkillNameAndSkillIdNotProvided(BadRequest):
    DETAIL = ErrorCode.SKILL_NAME_AND_SKILL_ID_NOT_PROVIDED
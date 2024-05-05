from src.job_profiles.constants import ErrorCode
from src.exceptions import BadRequest, NotFound

class JobProfileNotFound(NotFound):
    DETAIL = ErrorCode.JOB_PROFILE_NOT_FOUND

class JobProfileAlreadyExists(BadRequest):
    DETAIL = ErrorCode.JOB_PROFILE_ALREADY_EXISTS

class SkillAlreadyInJobProfile(BadRequest):
    DETAIL = ErrorCode.SKILL_ALREADY_IN_JOB_PROFILE

class SkillTagAlreadyAssigned(BadRequest):
    DETAIL = ErrorCode.SKILL_ALREADY_ASSIGNED_TO_JOB_PROFILE

class SkillNotAssignedToJobProfile(BadRequest):
    DETAIL = ErrorCode.SKILL_NOT_ASSIGNED_TO_JOB_PROFILE
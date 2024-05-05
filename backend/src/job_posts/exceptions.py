from src.job_posts.constants import ErrorCode 
from src.exceptions import BadRequest, NotFound, PermissionDenied

class JobPostNotFound(NotFound):
    DETAIL = ErrorCode.JOB_POST_NOT_FOUND

class JobPostNotVisible(PermissionDenied):
    DETAIL = ErrorCode.JOB_POST_VISIBLITY_EXCEPTION

class NotAStudent(PermissionDenied):
    DETAIL = ErrorCode.NOT_A_STUDENT

class JobApplicationAlreadyExists(BadRequest):
    DETAIL = ErrorCode.JOB_APPLICATION_ALREADY_EXISTS

class SkillAlreadyAssignedToJobPost(BadRequest):
    DETAIL = ErrorCode.SKILL_ALREADY_ASSIGNED_TO_JOB_POST

class SkillNotAssignedToJobPost(BadRequest):
    DETAIL = ErrorCode.SKILL_NOT_ASSIGNED_TO_JOB_POST

class JobPostAlreadySaved(BadRequest):
    DETAIL = ErrorCode.JOB_POST_ALREADY_SAVED

class JobPostNotSaved(BadRequest):
    DETAIL = ErrorCode.JOB_POST_NOT_SAVED
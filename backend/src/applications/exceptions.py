from src.applications.constants import ErrorCode
from src.exceptions import BadRequest, NotFound, NotFound, PermissionDenied

class JobApplicationNotFound(NotFound):
    DETAIL = ErrorCode.JOB_APPLICATION_NOT_FOUND

class JobApplicationAlreadyExists(BadRequest):
    DETAIL = ErrorCode.JOB_APPLICATION_ALREADY_EXISTS

class JobApplicationStageInvalid(BadRequest):
    DETAIL = ErrorCode.JOB_APPLICATION_STAGE_INVALID

class JobApplicationActivityNotFound(NotFound):
    DETAIL = ErrorCode.JOB_APPLICATION_ACTIVITY_NOT_FOUND

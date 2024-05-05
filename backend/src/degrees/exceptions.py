from src.degrees.constants import ErrorCode
from src.exceptions import NotFound

class DegreeNotFound(NotFound):
    DETAIL = ErrorCode.DEGREE_NOT_FOUND


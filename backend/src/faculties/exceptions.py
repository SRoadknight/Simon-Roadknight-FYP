from src.exceptions import NotFound 
from src.faculties.constants import ErrorCode

class FacultyNotFound(NotFound):
    DETAIL = ErrorCode.FACULTY_NOT_FOUND
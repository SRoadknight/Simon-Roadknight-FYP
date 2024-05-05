from src.schools_departments.constants import ErrorCode
from src.exceptions import NotFound 

class SchoolDepartmentNotFound(NotFound):
    DETAIL = ErrorCode.SCHOOL_DEPARTMENT_NOT_FOUND
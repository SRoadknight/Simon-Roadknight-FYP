from typing import Dict 
from src.auth.models import UserType
from src.job_posts.models import JobSource, Visbility

# map user to job post source
source_mapping: Dict[UserType, JobSource] = {
    UserType.STUDENT: JobSource.STUDENT,
    UserType.COMPANY: JobSource.COMPANY,
    UserType.STAFF: JobSource.INTERNAL_STAFF
}

# map JobSource to Visibility
visibility_mapping: Dict[JobSource, Visbility] = {
    JobSource.STUDENT: Visbility.PRIVATE,
    JobSource.COMPANY: Visbility.PUBLIC,
    JobSource.INTERNAL_STAFF: Visbility.PUBLIC
}
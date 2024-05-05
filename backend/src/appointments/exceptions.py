from src.appointments.constants import ErrorCode
from src.exceptions import NotFound, BadRequest, PermissionDenied

class AppointmentNotFound(NotFound):
    DETAIL = ErrorCode.APPOINTMENT_NOT_FOUND

class AppointmentSlotNotAvailable(BadRequest):
    DETAIL = ErrorCode.APPOINTMENT_SLOT_NOT_AVAILABLE

class AuthorisationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORISATION_FAILED

class SkillAlreadyAssignedToAppointment(BadRequest):
    DETAIL = ErrorCode.SKILL_ALREADY_ASSIGNED_TO_APPOINTMENT

class SkillNotAssignedToAppointment(BadRequest):
    DETAIL = ErrorCode.SKILL_NOT_ASSIGNED_TO_APPOINTMENT

class AppointmentAlreadyCancelled(BadRequest):
    DETAIL = ErrorCode.APPOINTMENT_ALREADY_CANCELLED

class StudentNotBookedForAppointment(BadRequest):
    DETAIL = ErrorCode.STUDENT_NOT_BOOKED_FOR_APPOINTMENT

class AppointmentsOverlap(BadRequest):
    DETAIL = ErrorCode.APPOINTMENT_OVERLAPS_WITH_EXISTING_APPOINTMENT


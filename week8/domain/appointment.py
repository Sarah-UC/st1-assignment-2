"""Appointment information and rules."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Iterable

from .patient import Patient
from .practitioner import Practitioner


class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class AppointmentDetails:
    appointment_id: str
    patient: Patient
    practitioner: Practitioner
    appointment_time: datetime


class Appointment:
    def __init__(
        self,
        appointment_id: str,
        patient: Patient,
        practitioner: Practitioner,
        appointment_time: datetime,
        status: AppointmentStatus = AppointmentStatus.SCHEDULED,
    ) -> None:
        if not appointment_id.strip():
            raise ValueError("Appointment ID cannot be empty.")
        if not isinstance(patient, Patient) or not isinstance(practitioner, Practitioner):
            raise TypeError("An appointment needs a Patient and a Practitioner.")
        if not isinstance(appointment_time, datetime):
            raise TypeError("Appointment time must be a datetime.")
        if not isinstance(status, AppointmentStatus):
            raise TypeError("Status must be an AppointmentStatus.")
        self.appointment_id = appointment_id.strip()
        self.patient = patient
        self.practitioner = practitioner
        self.appointment_time = appointment_time
        self._status = status

    @property
    def status(self) -> AppointmentStatus:
        return self._status

    def check_duplicate_booking(self, appointments: Iterable["Appointment"]) -> bool:
        """Return whether this slot is already booked for this practitioner."""
        return any(
            existing.appointment_id != self.appointment_id
            and existing.status is AppointmentStatus.SCHEDULED
            and existing.practitioner.identifier == self.practitioner.identifier
            and existing.appointment_time == self.appointment_time
            for existing in appointments
        )

    def update_status(self, new_status: AppointmentStatus) -> None:
        if not isinstance(new_status, AppointmentStatus):
            raise TypeError("Status must be an AppointmentStatus.")
        if self._status is AppointmentStatus.CANCELLED:
            raise ValueError("A cancelled appointment cannot be changed.")
        if new_status is not AppointmentStatus.CANCELLED:
            raise ValueError("The only supported status change is cancellation.")
        self._status = new_status

    def cancel_appointment(self) -> None:
        self.update_status(AppointmentStatus.CANCELLED)

    def view_history(self) -> AppointmentDetails:
        return AppointmentDetails(
            self.appointment_id,
            self.patient,
            self.practitioner,
            self.appointment_time,
        )

"""Coordinates appointment use cases."""

from datetime import datetime

from domain.appointment import Appointment, AppointmentStatus
from domain.patient import Patient
from domain.practitioner import Practitioner
from repositories.appointment_repository import AppointmentRepository


class DuplicateBookingError(ValueError):
    """Raised when a practitioner already has an appointment at that time."""


class AppointmentService:
    def __init__(self, repository: AppointmentRepository) -> None:
        self._repository = repository

    def book_appointment(
        self,
        appointment_id: str,
        patient: Patient,
        practitioner: Practitioner,
        appointment_time: datetime,
    ) -> Appointment:
        if self._repository.find_by_id(appointment_id) is not None:
            raise ValueError(f"Appointment {appointment_id} already exists.")
        appointment = Appointment(appointment_id, patient, practitioner, appointment_time)
        if appointment.check_duplicate_booking(self._repository.list_all()):
            raise DuplicateBookingError("This practitioner is already booked at that time.")
        self._repository.save(appointment)
        return appointment

    def find_appointment(self, appointment_id: str) -> Appointment | None:
        return self._repository.find_by_id(appointment_id)

    def appointment_history(self) -> list[Appointment]:
        return self._repository.list_all()

    def cancel_appointment(self, appointment_id: str) -> Appointment:
        appointment = self._repository.find_by_id(appointment_id)
        if appointment is None:
            raise ValueError(f"Appointment {appointment_id} was not found.")
        appointment.cancel_appointment()
        self._repository.save(appointment)
        return appointment

    def view_practitioner_appointments(self, practitioner_id: str) -> list[Appointment]:
        return [
            item
            for item in self._repository.list_all()
            if item.practitioner.identifier == practitioner_id
            and item.status is AppointmentStatus.SCHEDULED
        ]

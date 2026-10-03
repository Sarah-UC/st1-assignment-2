"""The small storage contract needed by AppointmentService."""

from typing import Protocol

from domain.appointment import Appointment


class AppointmentRepository(Protocol):
    def save(self, appointment: Appointment) -> None: ...

    def find_by_id(self, appointment_id: str) -> Appointment | None: ...

    def list_all(self) -> list[Appointment]: ...

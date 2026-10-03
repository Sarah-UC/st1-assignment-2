"""SQLite storage for appointment records."""

import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

from domain.appointment import Appointment, AppointmentStatus
from domain.patient import Patient
from domain.practitioner import Practitioner


class SQLiteAppointmentRepository:
    def __init__(self, database_path: str | Path = "smartcare.db") -> None:
        self.database_path = str(database_path)
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def _create_table(self) -> None:
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    patient_name TEXT NOT NULL,
                    practitioner_id TEXT NOT NULL,
                    practitioner_name TEXT NOT NULL,
                    specialty TEXT NOT NULL,
                    appointment_time TEXT NOT NULL,
                    status TEXT NOT NULL
                )"""
            )

    def save(self, appointment: Appointment) -> None:
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """INSERT INTO appointments VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(appointment_id) DO UPDATE SET
                    patient_id = excluded.patient_id,
                    patient_name = excluded.patient_name,
                    practitioner_id = excluded.practitioner_id,
                    practitioner_name = excluded.practitioner_name,
                    specialty = excluded.specialty,
                    appointment_time = excluded.appointment_time,
                    status = excluded.status""",
                (
                    appointment.appointment_id,
                    appointment.patient.patient_id,
                    appointment.patient.name,
                    appointment.practitioner.identifier,
                    appointment.practitioner.name,
                    appointment.practitioner.specialty,
                    appointment.appointment_time.isoformat(),
                    appointment.status.value,
                ),
            )

    def find_by_id(self, appointment_id: str) -> Appointment | None:
        with closing(self._connect()) as connection, connection:
            row = connection.execute(
                "SELECT * FROM appointments WHERE appointment_id = ?", (appointment_id,)
            ).fetchone()
        return self._to_appointment(row) if row else None

    def list_all(self) -> list[Appointment]:
        with closing(self._connect()) as connection, connection:
            rows = connection.execute(
                "SELECT * FROM appointments ORDER BY appointment_time, appointment_id"
            ).fetchall()
        return [self._to_appointment(row) for row in rows]

    @staticmethod
    def _to_appointment(row: tuple) -> Appointment:
        (
            appointment_id,
            patient_id,
            patient_name,
            practitioner_id,
            practitioner_name,
            specialty,
            appointment_time,
            status,
        ) = row
        return Appointment(
            appointment_id,
            Patient(patient_id, patient_name),
            Practitioner(practitioner_id, practitioner_name, specialty),
            datetime.fromisoformat(appointment_time),
            AppointmentStatus(status),
        )

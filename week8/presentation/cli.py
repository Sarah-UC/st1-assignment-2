"""Simple command-line interface for SmartCare appointments."""

from datetime import datetime

from domain.appointment import Appointment
from domain.patient import Patient
from domain.practitioner import Practitioner
from persistence.sqlite_appointment_repository import SQLiteAppointmentRepository
from services.appointment_service import AppointmentService


def _show(appointment: Appointment) -> None:
    print(
        f"{appointment.appointment_id} | {appointment.appointment_time:%Y-%m-%d %H:%M} | "
        f"{appointment.patient.name} | {appointment.practitioner.name} "
        f"({appointment.practitioner.specialty}) | {appointment.status.value}"
    )


def main() -> None:
    service = AppointmentService(SQLiteAppointmentRepository())
    while True:
        print("\nSmartCare appointments")
        print("1. Book appointment")
        print("2. Find appointment")
        print("3. View appointment history")
        print("4. View practitioner's scheduled appointments")
        print("5. Cancel appointment")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                appointment = service.book_appointment(
                    input("Appointment ID: ").strip(),
                    Patient(input("Patient ID: ").strip(), input("Patient name: ").strip()),
                    Practitioner(
                        input("Practitioner ID: ").strip(),
                        input("Practitioner name: ").strip(),
                        input("Specialty: ").strip(),
                    ),
                    datetime.strptime(input("Date and time (YYYY-MM-DD HH:MM): ").strip(), "%Y-%m-%d %H:%M"),
                )
                print("Appointment booked:")
                _show(appointment)
            elif choice == "2":
                appointment = service.find_appointment(input("Appointment ID: ").strip())
                print("Appointment found:" if appointment else "No matching appointment was found.")
                if appointment:
                    _show(appointment)
            elif choice == "3":
                appointments = service.appointment_history()
                if not appointments:
                    print("There is no appointment history yet.")
                for appointment in appointments:
                    _show(appointment)
            elif choice == "4":
                practitioner_id = input("Practitioner ID: ").strip()
                appointments = service.view_practitioner_appointments(practitioner_id)
                if not appointments:
                    print("No scheduled appointments were found for that practitioner.")
                for appointment in appointments:
                    _show(appointment)
            elif choice == "5":
                appointment = service.cancel_appointment(input("Appointment ID: ").strip())
                print("Appointment cancelled and retained in history:")
                _show(appointment)
            elif choice == "0":
                break
            else:
                print("Please choose one of the listed options.")
        except (ValueError, TypeError) as error:
            print(f"Could not complete that request: {error}")


if __name__ == "__main__":
    main()

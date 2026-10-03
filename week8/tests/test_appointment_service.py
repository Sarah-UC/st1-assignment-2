import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from domain.appointment import AppointmentStatus
from domain.patient import Patient
from domain.practitioner import Practitioner
from persistence.sqlite_appointment_repository import SQLiteAppointmentRepository
from services.appointment_service import AppointmentService, DuplicateBookingError

class AppointmentServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.repo=SQLiteAppointmentRepository(Path(self.tmp.name)/"test.db")
        self.service=AppointmentService(self.repo)
        self.patient=Patient("P1","Amina Otieno")
        self.doctor=Practitioner("D1","Dr Kamau","General")
        self.time=datetime(2026,10,5,9)
    def tearDown(self): self.tmp.cleanup()
    def test_booking_duplicate_find_and_history(self):
        item=self.service.book_appointment("A1",self.patient,self.doctor,self.time)
        with self.assertRaises(DuplicateBookingError): self.service.book_appointment("A2",self.patient,self.doctor,self.time)
        self.assertEqual(self.service.find_appointment("A1").appointment_id,"A1")
        self.assertEqual(len(self.service.appointment_history()),1)
        self.assertEqual(item.status,AppointmentStatus.SCHEDULED)
    def test_cancelled_record_stays_in_history_and_can_be_reloaded(self):
        self.service.book_appointment("A1",self.patient,self.doctor,self.time)
        self.service.cancel_appointment("A1")
        loaded=SQLiteAppointmentRepository(self.repo.database_path).find_by_id("A1")
        self.assertEqual(loaded.status,AppointmentStatus.CANCELLED)
        self.assertEqual(len(self.service.appointment_history()),1)

if __name__ == "__main__": unittest.main()

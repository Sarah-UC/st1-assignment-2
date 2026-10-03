import unittest
from datetime import datetime
from domain.appointment import Appointment, AppointmentStatus
from domain.patient import Patient
from domain.practitioner import Practitioner

class AppointmentTests(unittest.TestCase):
    def setUp(self):
        self.patient=Patient("P1","Amina Otieno")
        self.doctor=Practitioner("D1","Dr Kamau","General")
        self.time=datetime(2026,10,5,9)
    def test_matching_practitioner_and_time_is_duplicate(self):
        first=Appointment("A1",self.patient,self.doctor,self.time)
        another=Appointment("A2",self.patient,self.doctor,self.time)
        self.assertTrue(another.check_duplicate_booking([first]))
    def test_cancellation_changes_status_and_cannot_repeat(self):
        appt=Appointment("A1",self.patient,self.doctor,self.time)
        appt.cancel_appointment()
        self.assertEqual(appt.status,AppointmentStatus.CANCELLED)
        with self.assertRaises(ValueError): appt.cancel_appointment()

if __name__ == "__main__": unittest.main()

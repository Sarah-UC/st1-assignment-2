import unittest
from domain.practitioner import Practitioner

class PractitionerTests(unittest.TestCase):
    def test_practitioner_details_are_trimmed_and_recorded(self):
        doctor = Practitioner(" D1 ", " Dr Kamau ", " General ")
        self.assertEqual(doctor.record_practitioner_information(), "D1: Dr Kamau (General)")
    def test_empty_details_are_rejected(self):
        with self.assertRaises(ValueError): Practitioner("", "Dr Kamau", "General")
        with self.assertRaises(ValueError): Practitioner("D1", "Dr Kamau", " ")

if __name__ == "__main__": unittest.main()

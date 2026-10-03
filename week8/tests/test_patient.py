import unittest
from domain.patient import Patient

class PatientTests(unittest.TestCase):
    def test_patient_details_are_trimmed_and_recorded(self):
        patient = Patient(" P1 ", " Amina Otieno ")
        self.assertEqual(patient.record_patient_information(), "P1: Amina Otieno")
    def test_empty_details_are_rejected(self):
        with self.assertRaises(ValueError): Patient("", "Amina")
        with self.assertRaises(ValueError): Patient("P1", " ")

if __name__ == "__main__": unittest.main()

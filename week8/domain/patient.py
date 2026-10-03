"""Patient information and basic validation."""


class Patient:
    def __init__(self, patient_id: str, name: str) -> None:
        if not patient_id.strip():
            raise ValueError("Patient ID cannot be empty.")
        if not name.strip():
            raise ValueError("Patient name cannot be empty.")
        self.patient_id = patient_id.strip()
        self.name = name.strip()

    def record_patient_information(self) -> str:
        return f"{self.patient_id}: {self.name}"

    def find_patient_information(self) -> str:
        return self.record_patient_information()

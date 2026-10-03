"""Practitioner information and basic validation."""


class Practitioner:
    def __init__(self, identifier: str, name: str, specialty: str) -> None:
        if not identifier.strip():
            raise ValueError("Practitioner ID cannot be empty.")
        if not name.strip():
            raise ValueError("Practitioner name cannot be empty.")
        if not specialty.strip():
            raise ValueError("Practitioner specialty cannot be empty.")
        self.identifier = identifier.strip()
        self.name = name.strip()
        self.specialty = specialty.strip()

    def record_practitioner_information(self) -> str:
        return f"{self.identifier}: {self.name} ({self.specialty})"

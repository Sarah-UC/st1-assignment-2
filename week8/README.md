# SmartCare v0.5 Week 8

This project separates the appointment application into the layers requested in the Week 8 lab. The command-line interface handles user interaction, AppointmentService coordinates use cases, domain objects hold appointment rules, and a small repository contract separates the service from SQLite storage.

## Project layout

The `domain`, `services`, `repositories`, `persistence`, `presentation` and `tests` folders contain the implementation and checks. The three supplied Week 8 Word documents are kept at this folder’s root and completed as student work.

## Run the application

Use Python 3.10 or newer. The project has no third-party dependencies. From this folder run:

```bash
python -m presentation.cli
```

The SQLite database is created as `smartcare.db` in the current working directory. Appointment history includes cancelled records.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Architecture and evidence

`presentation/cli.py` calls `AppointmentService`. The service uses `AppointmentRepository`, a small Protocol implemented by `SQLiteAppointmentRepository` in the persistence package. Domain classes do not import SQLite or presentation code.

The supported duplicate rule is the same practitioner at the exact same datetime. The supplied requirements do not define appointment duration or overlapping-time behavior, so the implementation does not assume one.

The supplied Week 8 package contains v0.5 but not the v0.4 source or Weeks 4–7 source/workbooks. The completed Lab and Architecture Workbook state that limitation and do not make file-level claims about unavailable earlier code.

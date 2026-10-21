from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import PatientContact, Reminder


def test_SPEC001_AC3_unique_reminder_per_appointment(db):
    db.add(Reminder(appointment_id=1, status="sent", attempts=1, sent_at=datetime(2030, 1, 15, 9, 0)))
    db.commit()
    db.add(Reminder(appointment_id=1, status="sent", attempts=1))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()
    assert db.query(Reminder).count() == 1


def test_patient_contact_is_not_opted_out_by_default(db):
    db.add(PatientContact(patient_id=7, phone="+91-90000-00001"))
    db.commit()
    assert db.get(PatientContact, 7).opted_out is False

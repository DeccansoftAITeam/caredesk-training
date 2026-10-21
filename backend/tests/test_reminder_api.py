from datetime import datetime

import pytest

from app.main import app
from app.reminders.provider import FakeSmsProvider, SendResult
from app.routes.reminders import get_now, get_sms_provider

NOW = datetime(2030, 1, 15, 9, 0)


@pytest.fixture()
def provider(client):
    fake = FakeSmsProvider()
    app.dependency_overrides[get_sms_provider] = lambda: fake
    app.dependency_overrides[get_now] = lambda: NOW
    return fake


def book(client, patient_id=1, starts_at="2030-01-16T08:00:00"):
    resp = client.post(
        "/appointments",
        json={"patient_id": patient_id, "starts_at": starts_at, "duration_min": 30, "reason": "Check-up"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def set_contact(client, patient_id=1, phone="+91-90000-00001", opted_out=False):
    resp = client.put(f"/patients/{patient_id}/contact", json={"phone": phone, "opted_out": opted_out})
    assert resp.status_code == 200
    return resp.json()


def test_SPEC001_AC7_operator_sees_status_and_attempts_of_each_reminder(client, provider):
    appt_id = book(client)
    set_contact(client)
    provider.queue = [SendResult(ok=False, transient=True, error="503"), SendResult(ok=True)]

    run = client.post("/reminders/run")
    assert run.status_code == 200
    assert run.json() == {"sent": 1, "failed": 0, "skipped_opted_out": 0, "skipped_duplicate": 0}

    listing = client.get(f"/appointments/{appt_id}/reminders")
    assert listing.status_code == 200
    (reminder,) = listing.json()
    assert reminder["appointment_id"] == appt_id
    assert reminder["status"] == "sent"
    assert reminder["attempts"] == 2
    assert reminder["error"] is None


def test_SPEC001_AC7_failed_reminder_is_visible_with_its_error(client, provider):
    appt_id = book(client)
    set_contact(client)
    provider.queue = [SendResult(ok=False, transient=False, error="invalid number")]

    client.post("/reminders/run")

    (reminder,) = client.get(f"/appointments/{appt_id}/reminders").json()
    assert (reminder["status"], reminder["attempts"], reminder["error"]) == ("failed", 1, "invalid number")


def test_SPEC001_AC7_unknown_appointment_returns_a_problem_document(client, provider):
    resp = client.get("/appointments/999/reminders")
    assert resp.status_code == 404
    assert resp.json()["title"] == "Not Found"


def test_opting_out_through_the_api_stops_reminders(client, provider):
    appt_id = book(client)
    set_contact(client, opted_out=True)

    run = client.post("/reminders/run")

    assert run.json()["skipped_opted_out"] == 1
    assert provider.calls == 0
    assert client.get(f"/appointments/{appt_id}/reminders").json() == []


def test_contact_update_is_validated_and_idempotent(client, provider):
    assert client.put("/patients/1/contact", json={"phone": "1"}).status_code == 422
    first = set_contact(client, phone="+91-90000-00001")
    second = set_contact(client, phone="+91-90000-00002")
    assert first["patient_id"] == second["patient_id"] == 1
    assert second["phone"] == "+91-90000-00002"

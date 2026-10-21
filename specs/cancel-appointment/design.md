# Design: SPEC002 Cancel an appointment with a reason

Spec: specs/cancel-appointment/spec.md (Approved)

## What changes (architecture delta)
- New module `backend/app/cancellation.py` with `cancel_appointment(db, appointment_id, reason, now)`.
- New route `POST /appointments/{id}/cancel` in `backend/app/routes/cancellation.py`.
- The reminder service skips cancelled appointments.

## Data model and migration
Three columns are added to `appointments` by one generated Alembic revision (expand only):

| Column | Type | Notes |
|---|---|---|
| `cancelled_at` | timestamp, nullable | set when cancelled |
| `cancel_reason` | text up to 200, nullable | operator's reason |
| `cancelled_late` | boolean, not null | **server default false**, so existing rows stay valid |

The revision must be **generated against PostgreSQL**, not SQLite: autogenerate renders the boolean default for the
database it runs against, and the SQLite rendering (`0`) is rejected by PostgreSQL. A human reviews the generated
file; it is never edited by hand. A migration is a High-risk change.

## API and breaking changes
New: `POST /appointments/{id}/cancel` with body `{"reason": "..."}`. Appointment responses gain three optional fields
(`cancelled_at`, `cancel_reason`, `cancelled_late`); existing clients ignore them. No breaking change.

## Contracts between tasks
```python
# backend/app/models.py             (task T-002-01)
Appointment.cancelled_at: datetime | None
Appointment.cancel_reason: str | None
Appointment.cancelled_late: bool          # server default false

# backend/app/cancellation.py       (task T-002-02)
def cancel_appointment(db, appointment_id: int, reason: str, now: datetime) -> Appointment
LATE_WINDOW = timedelta(hours=24)

# backend/app/reminders/service.py  (task T-002-03)
# send_due_reminders ignores any appointment whose cancelled_at is set
```

## Threat-model delta
- The cancellation reason is operational free text and may contain personal or health details: it is stored, never sent
  by SMS, never written to logs or error messages.
- Abuse: any caller of the endpoint can cancel any appointment until authentication exists (stated out of scope).

## Test plan
| AC | Test layer | Test name pattern |
|---|---|---|
| SPEC002/AC-1 | integration and model | `test_SPEC002_AC1_*` |
| SPEC002/AC-2 | integration | `test_SPEC002_AC2_*` |
| SPEC002/AC-3 | integration | `test_SPEC002_AC3_*` |
| SPEC002/AC-4 | integration with a controlled clock, including the exact 24-hour boundary | `test_SPEC002_AC4_*` |
| SPEC002/AC-5 | unit | `test_SPEC002_AC5_*` |
| SPEC002/AC-6 | integration | `test_SPEC002_AC6_*` |

Acceptance tests are written first and reviewed by a human. The cancellation module must have no surviving mutants.

## Rollout and rollback
Additive columns and one new endpoint; nothing is switched on automatically. Rollback is to stop calling the endpoint;
the columns can stay. The migration has a tested downgrade.

## Decisions (ADR candidates)
- Keep the row and mark it (soft cancel) rather than delete: history and fee reporting survive.
- Late is computed once, at cancellation time, and stored, so a later policy change does not rewrite history.

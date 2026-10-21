# Tasks: SPEC002 Cancel an appointment with a reason

> This file IS the approved plan. An agent in **Delegated mode** may only execute a task whose approval block is
> signed, and may only touch the files listed in that task's "Files in scope". If the agent needs to leave scope
> it STOPS and asks. It never widens scope itself. One task = one branch = one worktree = one pull request.

| ID | Title | Depends on | Mode | Risk | Status |
|---|---|---|---|---|---|
| T-002-01 | Cancellation columns and migration | - | Delegated | High | Todo |
| T-002-02 | Cancellation logic and endpoint | T-002-01 | Delegated | Medium | Todo |
| T-002-03 | Skip cancelled appointments in reminders | T-002-01 | Delegated | Medium | Todo |

T-002-02 and T-002-03 are independent once T-002-01 is merged and can run in parallel worktrees.

---

## T-002-01: Cancellation columns and migration

- **Goal:** Add `cancelled_at`, `cancel_reason` and `cancelled_late` (server default false) to `appointments`.
- **ACs covered:** SPEC002/AC-1
- **Mode:** Delegated | **Risk:** High (database migration) | **Branch:** `agent/T-002-01-cancel-columns`
- **Budget:** 40 tool calls, 20 minutes
- **Inputs:** specs/cancel-appointment/design.md ("Data model and migration" and "Contracts between tasks")
- **Files in scope:** backend/app/models.py, backend/migrations/0003_*.py (generated), backend/tests/test_cancellation_model.py
- **Out of scope:** hand-editing a migration, any other model, CI config, auth
- **Done criteria:**
  - [ ] Human-reviewed acceptance test `test_SPEC002_AC1_*` passes
  - [ ] The revision was generated with `alembic revision --autogenerate` AGAINST POSTGRESQL and reviewed (the boolean default is `false`)
  - [ ] `cd backend && uv run pytest -q` and `uv run ruff check .` pass
  - [ ] Progress file `.agents/progress/T-002-01.md` is up to date
  - [ ] Commits carry the Agent-* trailers; draft pull request opened
- **Escalate to a human when:** scope must widen, the migration cannot be generated cleanly, or a test can only pass by weakening it.
- **Approval:** Tech lead: Arjun Mehta  Date: 2026-10-23

## T-002-02: Cancellation logic and endpoint

- **Goal:** Implement `cancel_appointment` and `POST /appointments/{id}/cancel`, including the late rule and the error cases.
- **ACs covered:** SPEC002/AC-1, SPEC002/AC-2, SPEC002/AC-3, SPEC002/AC-4, SPEC002/AC-6
- **Mode:** Delegated | **Risk:** Medium | **Branch:** `agent/T-002-02-cancel-endpoint`
- **Budget:** 50 tool calls, 25 minutes
- **Inputs:** specs/cancel-appointment/spec.md, design.md ("Contracts between tasks"), the merged result of T-002-01
- **Files in scope:** backend/app/cancellation.py, backend/app/routes/cancellation.py, backend/app/schemas.py, backend/app/main.py, backend/tests/test_cancellation.py
- **Out of scope:** models, migrations, the reminder service, authentication
- **Done criteria:**
  - [ ] Human-reviewed acceptance tests for AC-1 to AC-4 and AC-6 pass, including the exact 24-hour boundary
  - [ ] Mutation testing on `app/cancellation.py` leaves no survivors
  - [ ] Errors use `AppError` (RFC 7807 bodies)
  - [ ] `cd backend && uv run pytest -q` and `uv run ruff check .` pass
  - [ ] Progress file `.agents/progress/T-002-02.md` is up to date
  - [ ] Commits carry the Agent-* trailers; draft pull request opened
- **Escalate to a human when:** scope must widen, a spec criterion looks wrong, or the reason would have to be logged.
- **Approval:** Tech lead: Arjun Mehta  Date: 2026-10-23

## T-002-03: Skip cancelled appointments in reminders

- **Goal:** Make `send_due_reminders` ignore appointments that have been cancelled.
- **ACs covered:** SPEC002/AC-5
- **Mode:** Delegated | **Risk:** Medium | **Branch:** `agent/T-002-03-skip-cancelled`
- **Budget:** 30 tool calls, 15 minutes
- **Inputs:** specs/cancel-appointment/design.md ("Contracts between tasks"), backend/app/reminders/service.py, the merged result of T-002-01
- **Files in scope:** backend/app/reminders/service.py, backend/tests/test_cancellation_reminders.py
- **Out of scope:** models, migrations, the cancellation endpoint
- **Done criteria:**
  - [ ] Human-reviewed acceptance test `test_SPEC002_AC5_*` passes, including that other appointments are still reminded
  - [ ] The existing reminder tests and the mutation run on `service.py` still pass
  - [ ] `cd backend && uv run pytest -q` and `uv run ruff check .` pass
  - [ ] Progress file `.agents/progress/T-002-03.md` is up to date
  - [ ] Commits carry the Agent-* trailers; draft pull request opened
- **Escalate to a human when:** scope must widen or a test can only pass by weakening it.
- **Approval:** Tech lead: Arjun Mehta  Date: 2026-10-23

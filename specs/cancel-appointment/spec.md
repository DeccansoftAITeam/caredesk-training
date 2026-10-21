# SPEC002: Cancel an appointment with a reason

Status: Approved  
Owner: Product owner (CareDesk)  
Risk tier: Medium (the migration task is High)

## Problem and outcome
Front-desk staff can book and move appointments but cannot cancel one, so cancelled slots stay blocked and patients
still receive reminders for visits that will not happen. Staff will cancel an appointment with a reason, the clinic will
know which cancellations came too late for the fee policy, and cancelled appointments will no longer be reminded.  
**Success measure:** zero reminders sent for cancelled appointments; every late cancellation flagged for the fee policy.

## User stories
- US-1: As a front-desk operator, I want to cancel an appointment with a reason, so that the slot is freed and the reason is on record.
- US-2: As a clinic manager, I want late cancellations marked, so that the clinic's cancellation-fee policy can be applied.
- US-3: As a patient, I do not want a reminder for an appointment that was cancelled.

## Acceptance criteria (EARS, one behaviour each)

| ID | Criterion | Test layer |
|---|---|---|
| SPEC002/AC-1 | When an operator cancels an appointment with a reason of at least 3 characters, the system shall mark it cancelled, record the reason and the cancellation time, and return the updated appointment. | integration |
| SPEC002/AC-2 | If the reason is missing or shorter than 3 characters, then the system shall reject the request with status 422 and leave the appointment unchanged. | integration |
| SPEC002/AC-3 | If the appointment is already cancelled, then the system shall respond with status 409 and keep the first cancellation unchanged. | integration |
| SPEC002/AC-4 | When an appointment is cancelled less than 24 hours before it starts, the system shall mark the cancellation as late. | integration |
| SPEC002/AC-5 | While an appointment is cancelled, the system shall not send a reminder for it. | unit |
| SPEC002/AC-6 | If the appointment does not exist, then the system shall respond with status 404 and a problem document. | integration |

Every criterion maps to at least one automated test whose name contains the AC id (for example `test_SPEC002_AC3_...`).

## Out of scope
- Charging the cancellation fee: this release only marks late cancellations.
- Un-cancelling, cancelling past appointments, and notifying the patient that the appointment was cancelled.
- Authentication for operator endpoints (follow-up before real use).

## Open questions (filled by grilling)

| # | Question | Owner | Resolved answer |
|---|---|---|---|
| 1 | What counts as late? | Product owner | Less than 24 hours before the start time, matching the clinic cancellation policy. Exactly 24 hours is not late (AC-4). |
| 2 | Can a cancellation be undone? | Product owner | Not in this release. A cancelled appointment stays cancelled; staff book a new one. |
| 3 | What happens to reminders already sent? | Tech lead | Nothing. Only future reminders are suppressed (AC-5); no message is sent about the cancellation. |
| 4 | Should the reason be free text? | Product owner | Yes, 3 to 200 characters. It is operational data, never sent to patients and never logged. |
| 5 | Is the appointment deleted? | Tech lead | No. It is kept with the cancellation fields so history and fee reports stay possible. |
| 6 | Which clock decides now? | Tech lead | The server clock, injected through the same dependency the reminder job uses so tests can control it. |

## Approval
Product owner: Priya Nair  Tech lead: Arjun Mehta  Date: 2026-10-23

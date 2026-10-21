# Capstone report: cancel an appointment with a reason

*Example written by the trainer. Your numbers will differ; what matters is that every section is filled with evidence.*

## Result
- Feature: SPEC002, six acceptance criteria, three tasks (one High-risk migration).
- Backend tests: 47 passed. Traceability: every criterion has a test.

## Gates
| Gate | Result |
|---|---|
| Scope guard (hook) | no out-of-scope edit attempted by the agents; one attempt blocked in the demo |
| Tests, ruff, mypy | pass |
| Mutation testing (`cancellation.py`, `service.py`) | 3 of 3 and 17 of 17 mutants killed |
| Headless review gate (`ci_review.py`) | pass on the feature branch; fails the flawed branch (blocker plus two high) |
| Independent reviewer subagent | approve with two nits |
| Human review | migration reviewed by two people |

## Findings caught
1. The first migration was generated against SQLite and rendered a boolean default of `0`, which PostgreSQL rejects. Caught while verifying on PostgreSQL; regenerated.
2. The first test suite had no test at exactly 24 hours, so a mutant moving the boundary survived. A boundary test killed it.
3. The review gate flagged an f-string SQL query and a logged phone number on the deliberately flawed branch.

## Cost and time
- Telemetry summary (from `scripts/otel_summary.py`): three delegated sessions, about $1.10 in total on Sonnet; about 40 minutes of wall-clock including human review.
- One headless review of a small diff costs about $0.01 on Haiku.

## What I would change
- Add authentication to the operator endpoints before any real use.
- Run the review gate as a required status check and calibrate it against human reviews for a month before trusting it.
- Track merge-without-rework and revert rate for agent-authored pull requests; do not track lines of code.

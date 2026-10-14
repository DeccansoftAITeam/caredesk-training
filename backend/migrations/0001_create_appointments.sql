-- Generated schema migration. DO NOT EDIT BY HAND.
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    starts_at TIMESTAMP NOT NULL,
    duration_min INTEGER NOT NULL DEFAULT 30,
    reason VARCHAR(200) NOT NULL
);
CREATE INDEX ix_appointments_patient_id ON appointments (patient_id);

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppointmentCreate(BaseModel):
    patient_id: int
    starts_at: datetime
    duration_min: int = 30
    reason: str


class AppointmentOut(AppointmentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int

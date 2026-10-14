from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    patient_id: int
    starts_at: datetime
    duration_min: int = 30
    reason: str = Field(min_length=3, max_length=200)


class RescheduleRequest(BaseModel):
    starts_at: datetime


class AppointmentOut(AppointmentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int

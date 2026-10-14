from fastapi import FastAPI

from app.db import Base, engine
from app.errors import AppError, app_error_handler
from app.routes import appointments

Base.metadata.create_all(engine)

app = FastAPI(title="CareDesk")
app.add_exception_handler(AppError, app_error_handler)
app.include_router(appointments.router)


@app.get("/health")
def health():
    return {"status": "ok"}

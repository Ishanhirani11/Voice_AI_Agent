# backend/main.py

import os
import uuid

from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from backend.services.agent import process_query
from backend.services.speech_agent import process_voice_query

from backend.tools.appointment_tools import (
    fetch_slots,
    book_appointment,
    retrieve_appointments,
    cancel_appointment,
    modify_appointment
)

from backend.db.init_db import init_db

from backend.config import (
    APP_NAME,
    VERSION,
    RECORDINGS_FOLDER
)


# ==========================================================
# Create FastAPI App
# ==========================================================

app = FastAPI(
    title=APP_NAME,
    version=VERSION
)


# ==========================================================
# CORS Middleware
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================================
# Startup Event
# ==========================================================

@app.on_event("startup")
def on_startup():
    """Initialize database and required directories."""
    init_db()
    os.makedirs(RECORDINGS_FOLDER, exist_ok=True)


# ==========================================================
# Request Schemas
# ==========================================================

class ChatRequest(BaseModel):
    session_id: str
    message: str


class BookRequest(BaseModel):
    name: str
    phone: str
    date: str
    time: str


class CancelRequest(BaseModel):
    phone: str
    date: str
    time: str


class ModifyRequest(BaseModel):
    phone: str
    old_date: str
    old_time: str
    new_date: str
    new_time: str


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def root():
    return {
        "message": f"{APP_NAME} is running."
    }


# ==========================================================
# Conversational Chat Endpoint
# ==========================================================

@app.post("/chat")
def chat(request: ChatRequest):

    result = process_query(
        request.session_id,
        request.message
    )

    return result


# ==========================================================
# Voice Endpoint
# ==========================================================

@app.post("/voice")
async def voice(
        session_id: str = "",
        audio: UploadFile = File(...)
):
    # Use provided session_id or generate one
    if not session_id:
        session_id = str(uuid.uuid4())

    # Sanitize filename to prevent path traversal
    safe_name = f"{uuid.uuid4()}.wav"
    input_path = os.path.join(
        RECORDINGS_FOLDER,
        safe_name
    )

    # Save uploaded audio
    content = await audio.read()
    with open(input_path, "wb") as buffer:
        buffer.write(content)

    result = await process_voice_query(
        session_id,
        input_path
    )

    # Clean up uploaded file
    try:
        os.remove(input_path)
    except OSError:
        pass

    return result


# ==========================================================
# Fetch Available Slots
# ==========================================================

@app.get("/slots")
def get_slots():
    return fetch_slots()


# ==========================================================
# Book Appointment
# ==========================================================

@app.post("/book")
def book(request: BookRequest):
    return book_appointment(
        request.name,
        request.phone,
        request.date,
        request.time
    )


# ==========================================================
# Retrieve Appointments
# ==========================================================

@app.get("/appointments")
def appointments(phone: str):
    return retrieve_appointments(phone)


# ==========================================================
# Cancel Appointment
# ==========================================================

@app.post("/cancel")
def cancel(request: CancelRequest):
    return cancel_appointment(
        request.phone,
        request.date,
        request.time
    )


# ==========================================================
# Modify Appointment
# ==========================================================

@app.put("/modify")
def modify(request: ModifyRequest):
    return modify_appointment(
        request.phone,
        request.old_date,
        request.old_time,
        request.new_date,
        request.new_time
    )


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": VERSION
    }
# backend/config.py

import os
from dotenv import load_dotenv

# ---------------------------------------------------
# Load .env variables
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# API Keys
# ---------------------------------------------------

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


# ---------------------------------------------------
# LLM Configuration
# ---------------------------------------------------

GROQ_MODEL = "llama-3.3-70b-versatile"

TEMPERATURE = 0


# ---------------------------------------------------
# Whisper Configuration
# ---------------------------------------------------

WHISPER_MODEL = "tiny"

WHISPER_COMPUTE_TYPE = "int8"


# ---------------------------------------------------
# Text-to-Speech Configuration
# ---------------------------------------------------

TTS_VOICE = "en-US-AriaNeural"

TTS_OUTPUT_FILE = "response.mp3"


# ---------------------------------------------------
# Audio Input
# ---------------------------------------------------

INPUT_AUDIO_FILE = "input.wav"


# ---------------------------------------------------
# Database
# ---------------------------------------------------

DATABASE_URL = "sqlite:///appointments.db"


# ---------------------------------------------------
# Conversation Memory
# ---------------------------------------------------

MAX_HISTORY = 10


# ---------------------------------------------------
# Logging
# ---------------------------------------------------

LOG_FILE = "backend/logs/agent.log"

LOG_LEVEL = "INFO"


# ---------------------------------------------------
# Folder Paths
# ---------------------------------------------------

RECORDINGS_FOLDER = "recordings"

STATIC_FOLDER = "static"

AVATAR_FOLDER = "static/avatar"

OUTPUT_VIDEO = "response.mp4"


# ---------------------------------------------------
# Default Avatar Video
# ---------------------------------------------------

DEFAULT_AVATAR_VIDEO = "static/avatar/avatar.mp4"


# ---------------------------------------------------
# FastAPI Configuration
# ---------------------------------------------------

API_HOST = "0.0.0.0"

API_PORT = 8000


# ---------------------------------------------------
# Streamlit Configuration
# ---------------------------------------------------

STREAMLIT_PORT = 8501


# ---------------------------------------------------
# Session Configuration
# ---------------------------------------------------

SESSION_TIMEOUT_MINUTES = 30


# ---------------------------------------------------
# Latency Goal
# ---------------------------------------------------

TARGET_RESPONSE_LATENCY = 3


# ---------------------------------------------------
# Application Info
# ---------------------------------------------------

APP_NAME = "Voice AI Healthcare Receptionist"

VERSION = "1.0.0"


# ---------------------------------------------------
# Feature Flags
# ---------------------------------------------------

ENABLE_SUMMARIZATION = True

ENABLE_VOICE = True

ENABLE_AVATAR = False

ENABLE_LOGGING = True
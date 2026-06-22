# 🩺 Voice AI Healthcare Receptionist

A production-style Voice AI Healthcare Receptionist built using FastAPI, Groq, Whisper, Streamlit, and SQLite.

The assistant supports:

* Voice interaction
* Multi-turn conversations
* Appointment booking and management
* Tool calling
* Session memory
* Conversation summaries
* Speech-to-text
* Text-to-speech
* Avatar support (Wav2Lip-ready)

---

# Features

## Conversational AI

* Groq Llama-3.3-70B
* Structured outputs using Pydantic
* Slot-filling conversation flow
* Multi-turn context memory
* Conversation summarization

---

## Appointment Management

Supports:

* Fetch available slots
* Book appointments
* Retrieve appointments
* Modify appointments
* Cancel appointments

---

## Speech Capabilities

### Speech-to-Text

Uses:

* Faster-Whisper
* Tiny model
* INT8 inference

### Text-to-Speech

Uses:

* edge-tts
* Microsoft Aria Neural voice

---

## Database

SQLite + SQLAlchemy

Stores:

* Appointments
* User information
* Persistent conversation memory (future)

---

## Frontend

Streamlit

Supports:

* Chat UI
* Voice input
* Audio playback
* Session history
* Avatar placeholder

---

# Architecture

```text
User Speech
      ↓
Whisper Tiny
      ↓
Groq Llama-3.3-70B
      ↓
Session Memory
      ↓
Summary Memory
      ↓
Tool Executor
      ↓
SQLite
      ↓
edge-tts
      ↓
response.mp3
      ↓
Wav2Lip
      ↓
response.mp4
      ↓
Streamlit
```

---

# Project Structure

```text
voice-ai-agent/

backend/
│
├── main.py
├── config.py
│
├── db/
│
├── models/
│
├── services/
│   ├── agent.py
│   ├── memory.py
│   ├── summary.py
│   ├── summarizer.py
│   ├── session.py
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   ├── speech_agent.py
│   ├── avatar.py
│   ├── video_generator.py
│   └── wav2lip.py
│
├── tools/
│
└── logs/

frontend/
│
└── app.py

recordings/

static/
└── avatar/

Dockerfile
docker-compose.yml
requirements.txt
README.md
.env
```

---

# Installation

## Clone Repository

```bash
git clone <repository_url>

cd voice-ai-agent
```

---

## Create Virtual Environment

### Mac/Linux

```bash
python3.11 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create:

```text
.env
```

Example:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

---

# Run Backend

```bash
uvicorn backend.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Run Frontend

```bash
streamlit run frontend/app.py
```

Default URL:

```text
http://localhost:8501
```

---

# Docker

Build:

```bash
docker compose build
```

Run:

```bash
docker compose up
```

Stop:

```bash
docker compose down
```

---

# API Endpoints

## Chat

```http
POST /chat
```

---

## Voice

```http
POST /voice
```

---

## Slots

```http
GET /slots
```

---

## Book Appointment

```http
POST /book
```

---

## Retrieve Appointments

```http
GET /appointments
```

---

## Modify Appointment

```http
PUT /modify
```

---

## Cancel Appointment

```http
DELETE /cancel
```

---

## Health Check

```http
GET /health
```

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* SQLite

## LLM

* Groq
* Llama-3.3-70B-Versatile

## Speech

* Faster-Whisper
* edge-tts

## Frontend

* Streamlit

## Validation

* Pydantic

## Deployment

* Docker
* Docker Compose

---

# Future Improvements

* Persistent memory
* LangGraph integration
* Redis cache
* Vector database memory
* Wav2Lip avatar generation
* Authentication
* Dockerized Streamlit service
* Cloud deployment

---

# Author

Ishan Hirani

B.Tech Artificial Intelligence & Data Science

Government Engineering College, Rajkot

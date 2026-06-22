# Voice AI Healthcare Receptionist Architecture

## Overall Flow

```text
User
 ↓
Microphone
 ↓
Whisper Tiny
 ↓
Speech-to-Text
 ↓
Agent
 ↓
Session Memory
 ↓
Conversation Summary
 ↓
Tool Executor
 ↓
SQLite
 ↓
Text Response
 ↓
edge-tts
 ↓
response.mp3
 ↓
Avatar Layer
 ↓
response.mp4
 ↓
Streamlit UI
```

---

## Backend Architecture

```text
FastAPI
│
├── /chat
├── /voice
├── /slots
├── /book
├── /appointments
├── /modify
└── /cancel
```

---

## Agent Architecture

```text
User Query
↓
Prompt
↓
Groq Llama-3.3-70B
↓
Pydantic Parsing
↓
Session State
↓
Slot Filling
↓
Tool Execution
↓
Response
```

---

## Memory Architecture

```text
Recent History
↓
Summary Generator
↓
Persistent Summary
↓
SQLite
```

---

## Voice Architecture

```text
input.wav
↓
Whisper Tiny
↓
Text
↓
Agent
↓
Response Text
↓
edge-tts
↓
response.mp3
```

---

## Avatar Architecture

```text
response.mp3
↓
Wav2Lip
↓
response.mp4
↓
Streamlit
```

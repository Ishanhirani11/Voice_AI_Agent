# frontend/app.py

import sys
import os

# Add the project root to sys.path so 'backend' module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import asyncio
import uuid

import requests
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from backend.services.speech_to_text import transcribe
from backend.services.text_to_speech import generate_audio


# =====================================================
# Configuration
# =====================================================

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Voice AI Healthcare Receptionist",
    page_icon="🩺",
    layout="wide"
)


# =====================================================
# Custom CSS for premium look
# =====================================================

st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
    }

    /* Tool call badges */
    .tool-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        margin: 4px 2px;
        animation: fadeIn 0.5s ease-in;
    }

    .tool-executing {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: #000;
    }

    .tool-completed {
        background: linear-gradient(135deg, #10b981, #059669);
        color: #fff;
    }

    .tool-failed {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: #fff;
    }

    .tool-waiting {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: #fff;
    }

    /* Summary card */
    .summary-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
    }

    /* Avatar container */
    .avatar-container {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1e1e3f, #2d2d5f);
        border-radius: 16px;
        border: 1px solid #3d3d7f;
    }

    .avatar-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        margin: 0 auto 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
    }

    .avatar-speaking {
        animation: pulse 1.5s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); transform: scale(1); }
        50% { box-shadow: 0 0 40px rgba(99, 102, 241, 0.6); transform: scale(1.05); }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #818cf8;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# Session State
# =====================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "tool_calls" not in st.session_state:
    st.session_state.tool_calls = []

if "summary" not in st.session_state:
    st.session_state.summary = None

if "is_speaking" not in st.session_state:
    st.session_state.is_speaking = False


# =====================================================
# Helper: Render tool call badges
# =====================================================

def render_tool_calls(tool_calls: list):
    """Display tool call status badges in the UI."""

    if not tool_calls:
        return

    for tc in tool_calls:
        tool_name = tc.get("tool", "unknown")
        status = tc.get("status", "executing")
        result_msg = tc.get("result", "")

        # Format tool name for display
        display_name = tool_name.replace("_", " ").title()

        if status == "executing":
            icon = "⏳"
            css_class = "tool-executing"
            label = f"{icon} {display_name}..."
        elif status == "completed":
            icon = "✅"
            css_class = "tool-completed"
            label = f"{icon} {display_name}"
        elif status == "failed":
            icon = "❌"
            css_class = "tool-failed"
            label = f"{icon} {display_name} Failed"
        elif status == "waiting_for_info":
            missing = tc.get("missing", [])
            icon = "📝"
            css_class = "tool-waiting"
            label = f"{icon} Waiting: {', '.join(missing)}"
        elif status == "generating_summary":
            icon = "📋"
            css_class = "tool-executing"
            label = f"{icon} Generating Summary..."
        else:
            icon = "🔧"
            css_class = "tool-executing"
            label = f"{icon} {display_name}"

        st.markdown(
            f'<span class="tool-badge {css_class}">{label}</span>',
            unsafe_allow_html=True
        )


# =====================================================
# Helper: Render summary
# =====================================================

def render_summary(summary_text: str):
    """Display conversation summary."""

    if not summary_text:
        return

    st.markdown("### 📋 Conversation Summary")

    try:
        summary_data = json.loads(summary_text)

        st.markdown('<div class="summary-card">', unsafe_allow_html=True)

        if summary_data.get("summary"):
            st.write(f"**Overview:** {summary_data['summary']}")

        if summary_data.get("patient_name"):
            st.write(f"**Patient:** {summary_data['patient_name']}")

        if summary_data.get("phone_number"):
            st.write(f"**Phone:** {summary_data['phone_number']}")

        if summary_data.get("appointments_booked"):
            st.write("**Booked:**")
            for appt in summary_data["appointments_booked"]:
                st.write(f"  ✅ {appt}")

        if summary_data.get("appointments_cancelled"):
            st.write("**Cancelled:**")
            for appt in summary_data["appointments_cancelled"]:
                st.write(f"  ❌ {appt}")

        if summary_data.get("appointments_modified"):
            st.write("**Modified:**")
            for appt in summary_data["appointments_modified"]:
                st.write(f"  🔄 {appt}")

        if summary_data.get("timestamp"):
            st.write(f"**Timestamp:** {summary_data['timestamp']}")

        st.markdown('</div>', unsafe_allow_html=True)

    except (json.JSONDecodeError, TypeError):
        st.info(summary_text)


# =====================================================
# Helper: Process via API
# =====================================================

def send_chat_message(session_id: str, message: str) -> dict:
    """Send a chat message to the backend API."""

    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "session_id": session_id,
                "message": message
            },
            timeout=30
        )
        return response.json()

    except Exception as e:
        return {
            "message": f"Connection error: {str(e)}",
            "tool_calls": []
        }


# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.title("🩺 Voice AI")
    st.caption("Healthcare Receptionist")

    st.divider()

    st.write(f"**Session:**")
    st.code(st.session_state.session_id[:8] + "...")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.tool_calls = []
        st.session_state.summary = None
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.divider()

    # Quick Actions
    st.markdown("**Quick Actions:**")

    if st.button("📅 View Slots", use_container_width=True):
        result = send_chat_message(
            st.session_state.session_id,
            "What appointment slots are available?"
        )
        st.session_state.messages.append({"role": "user", "content": "What appointment slots are available?"})
        st.session_state.messages.append({"role": "assistant", "content": result.get("message", "")})
        if result.get("tool_calls"):
            st.session_state.tool_calls.extend(result["tool_calls"])
        st.rerun()


# =====================================================
# Main Layout
# =====================================================

col_chat, col_avatar = st.columns([3, 1])


# =====================================================
# Avatar Column
# =====================================================

with col_avatar:
    speaking_class = "avatar-speaking" if st.session_state.is_speaking else ""

    st.markdown(f"""
    <div class="avatar-container">
        <div class="avatar-circle {speaking_class}">
            🩺
        </div>
        <h3 style="color: #c7d2fe; margin: 0;">Dr. AI</h3>
        <p style="color: #94a3b8; font-size: 14px;">Healthcare Assistant</p>
        <p style="color: {'#10b981' if not st.session_state.is_speaking else '#f59e0b'}; font-size: 12px;">
            {'🟢 Ready' if not st.session_state.is_speaking else '🔊 Speaking...'}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Show recent tool calls
    if st.session_state.tool_calls:
        st.markdown("---")
        st.markdown("**Recent Actions:**")
        # Show last 5 tool calls
        for tc in st.session_state.tool_calls[-5:]:
            render_tool_calls([tc])


# =====================================================
# Chat Column
# =====================================================

with col_chat:

    st.title("🩺 Voice AI Healthcare Receptionist")
    st.caption("Book, manage, and track your medical appointments")

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Text Chat Input
    prompt = st.chat_input("Type your message...")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = send_chat_message(
                    st.session_state.session_id,
                    prompt
                )

            assistant_message = result.get(
                "message", "Something went wrong."
            )

            # Show tool call badges
            tool_calls = result.get("tool_calls", [])
            if tool_calls:
                render_tool_calls(tool_calls)
                st.session_state.tool_calls.extend(tool_calls)

            st.markdown(assistant_message)

            # Check for summary
            if result.get("summary"):
                st.session_state.summary = result["summary"]

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_message}
        )

        st.rerun()


# =====================================================
# Voice Chat Section
# =====================================================

st.divider()

st.subheader("🎤 Voice Chat")

audio = mic_recorder(
    start_prompt="🎙 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="voice_input"
)

if audio:

    # Save audio temporarily
    input_path = f"input_{uuid.uuid4().hex[:8]}.wav"

    with open(input_path, "wb") as f:
        f.write(audio["bytes"])

    st.audio(input_path)

    with st.spinner("🎤 Transcribing speech..."):
        try:
            user_text = transcribe(input_path)
        except Exception:
            user_text = ""

    # Clean up audio file
    try:
        os.remove(input_path)
    except OSError:
        pass

    if user_text:
        st.session_state.messages.append(
            {"role": "user", "content": user_text}
        )

        with st.chat_message("user"):
            st.markdown(f"🎤 *{user_text}*")

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                result = send_chat_message(
                    st.session_state.session_id,
                    user_text
                )

            assistant_text = result.get(
                "response_text",
                result.get("message", "Something went wrong.")
            )

            # Show tool call badges
            tool_calls = result.get("tool_calls", [])
            if tool_calls:
                render_tool_calls(tool_calls)
                st.session_state.tool_calls.extend(tool_calls)

            st.markdown(assistant_text)

            # Generate TTS
            try:
                tts_path = f"response_{uuid.uuid4().hex[:8]}.mp3"
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(
                    generate_audio(assistant_text, tts_path)
                )
                loop.close()

                st.audio(tts_path)

                # Clean up TTS file after display
                try:
                    os.remove(tts_path)
                except OSError:
                    pass

            except Exception as e:
                st.warning(f"Could not generate voice: {str(e)}")

            # Check for summary
            if result.get("summary"):
                st.session_state.summary = result["summary"]

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_text}
        )

    else:
        st.warning("Could not understand the audio. Please try again.")


# =====================================================
# Summary Section
# =====================================================

if st.session_state.summary:
    st.divider()
    render_summary(st.session_state.summary)


# =====================================================
# Metrics Footer
# =====================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💬 Messages",
        len(st.session_state.messages)
    )

with col2:
    st.metric(
        "🔧 Tool Calls",
        len(st.session_state.tool_calls)
    )

with col3:
    st.metric(
        "📡 Status",
        "Active"
    )
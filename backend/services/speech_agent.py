# backend/services/speech_agent.py

import os
import uuid
import asyncio

from backend.services.agent import process_query
from backend.services.speech_to_text import transcribe
from backend.services.text_to_speech import generate_audio
from backend.config import (
    RECORDINGS_FOLDER,
    TTS_OUTPUT_FILE
)


# ---------------------------------------------------
# Ensure recordings directory exists
# ---------------------------------------------------

os.makedirs(
    RECORDINGS_FOLDER,
    exist_ok=True
)


# ---------------------------------------------------
# Main Voice Pipeline
# ---------------------------------------------------

async def process_voice_query(
        session_id: str,
        audio_path: str
):
    """
    Complete voice pipeline.

    audio
        ↓
    Whisper
        ↓
    Agent
        ↓
    edge-tts
        ↓
    response.mp3
    """

    # ---------------------------------------------
    # Speech → Text
    # ---------------------------------------------

    user_text = transcribe(
        audio_path
    )

    # Handle empty transcription

    if not user_text:

        response_text = (
            "Sorry, I could not understand what you said."
        )

        response_audio = await generate_audio(
            response_text
        )

        return {

            "success": False,

            "user_text": "",

            "response_text": response_text,

            "response_audio": response_audio
        }

    # ---------------------------------------------
    # Text → Agent
    # ---------------------------------------------

    agent_result = process_query(
        session_id,
        user_text
    )

    response_text = agent_result.get(
        "message",
        "Sorry, something went wrong."
    )

    # ---------------------------------------------
    # Text → Speech
    # ---------------------------------------------

    response_audio = await generate_audio(
        response_text
    )

    # ---------------------------------------------
    # Final Response
    # ---------------------------------------------

    return {

        "success": True,

        "user_text": user_text,

        "response_text": response_text,

        "response_audio": response_audio,

        "latency": agent_result.get(
            "latency",
            None
        )
    }


# ---------------------------------------------------
# Process Raw Text Through TTS Only
# ---------------------------------------------------

async def text_to_voice(
        text: str
):
    """
    Convert text directly to speech.
    """

    audio_path = await generate_audio(
        text
    )

    return {

        "text": text,

        "audio": audio_path
    }


# ---------------------------------------------------
# Process Audio Without Session Memory
# ---------------------------------------------------

async def process_single_audio(
        audio_path: str
):
    """
    Stateless voice processing.
    """

    session_id = str(
        uuid.uuid4()
    )

    result = await process_voice_query(
        session_id,
        audio_path
    )

    return result


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    async def main():

        result = await process_voice_query(
            session_id="user_1",
            audio_path="sample.wav"
        )

        print()

        print("User Speech:")
        print(result["user_text"])

        print()

        print("Assistant Response:")
        print(result["response_text"])

        print()

        print("Audio File:")
        print(result["response_audio"])


    asyncio.run(main())
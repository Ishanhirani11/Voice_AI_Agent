# backend/services/text_to_speech.py

import edge_tts

from backend.config import (
    TTS_VOICE,
    TTS_OUTPUT_FILE
)


# ---------------------------------------------------
# Generate Speech
# ---------------------------------------------------

async def generate_audio(
        text: str,
        output_path: str = TTS_OUTPUT_FILE
) -> str:
    """
    Convert text into speech and save as MP3.

    Parameters
    ----------
    text : str
        Text to convert to speech.

    output_path : str
        Output MP3 path.

    Returns
    -------
    str
        Path to generated audio.
    """

    communicate = edge_tts.Communicate(
        text=text,
        voice=TTS_VOICE
    )

    await communicate.save(
        output_path
    )

    return output_path


# ---------------------------------------------------
# Generate Speech with Custom Voice
# ---------------------------------------------------

async def generate_audio_with_voice(
        text: str,
        voice: str,
        output_path: str = TTS_OUTPUT_FILE
) -> str:

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    await communicate.save(
        output_path
    )

    return output_path


# ---------------------------------------------------
# Available Voices
# ---------------------------------------------------

async def get_available_voices():

    voices = await edge_tts.list_voices()

    return voices


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    import asyncio


    async def main():

        output_file = await generate_audio(
            "Hello, I am your healthcare receptionist."
        )

        print()
        print("Audio saved at:")
        print(output_file)


    asyncio.run(main())
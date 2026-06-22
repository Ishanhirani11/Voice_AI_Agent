# backend/services/speech_to_text.py

from faster_whisper import WhisperModel

from backend.config import (
    WHISPER_MODEL,
    WHISPER_COMPUTE_TYPE
)


# ---------------------------------------------------
# Load Whisper Model
# ---------------------------------------------------

model = WhisperModel(
    WHISPER_MODEL,
    compute_type=WHISPER_COMPUTE_TYPE
)


# ---------------------------------------------------
# Transcribe Audio File
# ---------------------------------------------------

def transcribe(audio_path: str) -> str:
    """
    Convert speech audio into text.

    Parameters
    ----------
    audio_path : str
        Path to audio file.

    Returns
    -------
    str
        Transcribed text.
    """

    segments, info = model.transcribe(
        audio_path
    )

    text = ""

    for segment in segments:

        text += segment.text

    return text.strip()


# ---------------------------------------------------
# Detailed Transcription
# ---------------------------------------------------

def transcribe_with_metadata(
        audio_path: str
):
    """
    Returns full transcription metadata.
    """

    segments, info = model.transcribe(
        audio_path
    )

    results = []

    for segment in segments:

        results.append(
            {
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip()
            }
        )

    return {
        "language": info.language,
        "language_probability": round(
            info.language_probability,
            3
        ),
        "segments": results
    }


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    audio_file = "sample.wav"

    text = transcribe(
        audio_file
    )

    print()

    print("Transcribed Text:")

    print(text)
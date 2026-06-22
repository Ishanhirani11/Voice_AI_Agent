# backend/services/wav2lip.py

"""
Wav2Lip wrapper.

Currently this is a placeholder implementation.

Later you can connect it to the real Wav2Lip repository
without changing the rest of the application.
"""

import os
import subprocess

from backend.config import (
    DEFAULT_AVATAR_VIDEO,
    OUTPUT_VIDEO
)


# ---------------------------------------------------
# Generate Talking Avatar
# ---------------------------------------------------

def generate_lip_sync_video(
        audio_path: str,
        face_path: str = DEFAULT_AVATAR_VIDEO,
        output_path: str = OUTPUT_VIDEO
):
    """
    Generate a lip-synced video.

    Parameters
    ----------
    audio_path : str
        Path to response audio.

    face_path : str
        Avatar image or video.

    output_path : str
        Output mp4 file.

    Returns
    -------
    str
        Generated video path.
    """

    #
    # Placeholder implementation
    #
    # Replace this section later with real Wav2Lip
    #

    if not os.path.exists(face_path):

        raise FileNotFoundError(
            f"Face file not found: {face_path}"
        )

    # For now just return the avatar video
    return face_path


# ---------------------------------------------------
# Real Wav2Lip Command
# ---------------------------------------------------

def run_wav2lip(
        checkpoint_path: str,
        face_path: str,
        audio_path: str,
        output_path: str = OUTPUT_VIDEO
):
    """
    Execute Wav2Lip inference.

    Example command:

    python inference.py
        --checkpoint_path checkpoints/wav2lip_gan.pth
        --face face.mp4
        --audio response.mp3
        --outfile response.mp4
    """

    command = [

        "python",

        "inference.py",

        "--checkpoint_path",
        checkpoint_path,

        "--face",
        face_path,

        "--audio",
        audio_path,

        "--outfile",
        output_path
    ]

    subprocess.run(
        command,
        check=True
    )

    return output_path


# ---------------------------------------------------
# Check Output Video
# ---------------------------------------------------

def output_exists():

    return os.path.exists(
        OUTPUT_VIDEO
    )


# ---------------------------------------------------
# Delete Output
# ---------------------------------------------------

def remove_output():

    if os.path.exists(
            OUTPUT_VIDEO
    ):

        os.remove(
            OUTPUT_VIDEO
        )


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    print()

    print(
        "Output Exists:",
        output_exists()
    )
# backend/services/video_generator.py

import os
import shutil

from backend.config import (
    DEFAULT_AVATAR_VIDEO,
    OUTPUT_VIDEO
)


# ---------------------------------------------------
# Generate Avatar Video
# ---------------------------------------------------

def generate_avatar_video(
        audio_path: str,
        output_path: str = OUTPUT_VIDEO
):
    """
    Generate a response video.

    Currently this uses a placeholder avatar video.

    Later this file can be replaced by Wav2Lip
    without changing the rest of the application.

    Parameters
    ----------
    audio_path : str
        Path to response audio.

    output_path : str
        Path to generated video.

    Returns
    -------
    str
        Output video path.
    """

    # Ensure source avatar video exists

    if not os.path.exists(
            DEFAULT_AVATAR_VIDEO
    ):

        raise FileNotFoundError(
            f"Avatar video not found: "
            f"{DEFAULT_AVATAR_VIDEO}"
        )

    # Copy placeholder video

    shutil.copy(
        DEFAULT_AVATAR_VIDEO,
        output_path
    )

    return output_path


# ---------------------------------------------------
# Check Avatar Source
# ---------------------------------------------------

def avatar_video_exists():

    return os.path.exists(
        DEFAULT_AVATAR_VIDEO
    )


# ---------------------------------------------------
# Delete Generated Video
# ---------------------------------------------------

def remove_generated_video():

    if os.path.exists(
            OUTPUT_VIDEO
    ):

        os.remove(
            OUTPUT_VIDEO
        )


# ---------------------------------------------------
# Get Output Video
# ---------------------------------------------------

def get_generated_video():

    if os.path.exists(
            OUTPUT_VIDEO
    ):

        return OUTPUT_VIDEO

    return None


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    print()

    print(
        "Avatar Source Exists:",
        avatar_video_exists()
    )

    print()

    print(
        "Generated Video:",
        get_generated_video()
    )
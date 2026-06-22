# backend/services/avatar.py

import os

from backend.services.video_generator import (
    generate_avatar_video
)

from backend.config import (
    OUTPUT_VIDEO,
    ENABLE_AVATAR
)


# ---------------------------------------------------
# Create Avatar Video
# ---------------------------------------------------

def create_avatar(
        audio_path: str,
        output_path: str = OUTPUT_VIDEO
):
    """
    Generate an avatar video from speech audio.

    Parameters
    ----------
    audio_path : str
        Path to response audio.

    output_path : str
        Path to output video.

    Returns
    -------
    str
        Generated video path.
    """

    if not ENABLE_AVATAR:

        return None

    video_path = generate_avatar_video(
        audio_path,
        output_path
    )

    return video_path


# ---------------------------------------------------
# Check Avatar Availability
# ---------------------------------------------------

def avatar_available():

    return ENABLE_AVATAR


# ---------------------------------------------------
# Get Latest Avatar Video
# ---------------------------------------------------

def get_avatar_video():

    if os.path.exists(
            OUTPUT_VIDEO
    ):

        return OUTPUT_VIDEO

    return None


# ---------------------------------------------------
# Remove Generated Video
# ---------------------------------------------------

def delete_avatar_video():

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
        "Avatar Enabled:",
        avatar_available()
    )

    print()

    print(
        "Latest Video:",
        get_avatar_video()
    )
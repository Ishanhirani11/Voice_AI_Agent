# backend/services/healthcheck.py

import os

from backend.config import (
    GROQ_API_KEY
)


def check_groq():

    return GROQ_API_KEY is not None


def check_database():

    return os.path.exists(
        "appointments.db"
    )


def check_logs():

    return os.path.exists(
        "backend/logs"
    )


def check_recordings():

    return os.path.exists(
        "recordings"
    )


def system_health():

    return {

        "groq_api":

            check_groq(),

        "database":

            check_database(),

        "logs":

            check_logs(),

        "recordings":

            check_recordings()
    }


if __name__ == "__main__":

    print()

    print(
        system_health()
    )
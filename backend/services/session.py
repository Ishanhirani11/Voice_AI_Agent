# backend/services/session.py

DEFAULT_STATE = {
    "intent": None,

    "name": None,
    "phone": None,

    "date": None,
    "time": None,

    "old_date": None,
    "old_time": None,

    "new_date": None,
    "new_time": None
}

all_sessions = {}


def get_state(session_id: str):

    if session_id not in all_sessions:
        all_sessions[session_id] = DEFAULT_STATE.copy()

    return all_sessions[session_id]


def update_state(session_id: str, data: dict):

    state = get_state(session_id)

    for key, value in data.items():

        if (
            key in state
            and value is not None
            and value != ""
        ):
            state[key] = value


def clear_state(session_id: str):

    all_sessions[session_id] = DEFAULT_STATE.copy()
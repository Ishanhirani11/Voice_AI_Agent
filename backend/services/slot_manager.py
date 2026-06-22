# backend/services/slot_manager.py

REQUIRED_SLOTS = {

    "book_appointment": [
        "name",
        "phone",
        "date",
        "time"
    ],

    "cancel_appointment": [
        "phone",
        "date",
        "time"
    ],

    "modify_appointment": [
        "phone",
        "old_date",
        "old_time",
        "new_date",
        "new_time"
    ],

    "retrieve_appointments": [
        "phone"
    ]
}


QUESTIONS = {

    "name":
        "May I have your name?",

    "phone":
        "Could you tell me your phone number?",

    "date":
        "Which date would you prefer?",

    "time":
        "What time would you like?",

    "old_date":
        "Which appointment date would you like to modify?",

    "old_time":
        "What was the previous appointment time?",

    "new_date":
        "What is the new date?",

    "new_time":
        "What is the new preferred time?"
}


def get_missing_slots(intent, state):

    required = REQUIRED_SLOTS.get(intent, [])

    missing = []

    for slot in required:

        if not state.get(slot):
            missing.append(slot)

    return missing
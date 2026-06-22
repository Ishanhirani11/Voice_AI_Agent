from backend.services.slot_manager import (
    get_missing_slots,
    QUESTIONS
)


def handle_slot_filling(
        intent,
        state
):

    missing_slots = get_missing_slots(
        intent,
        state
    )

    if missing_slots:

        next_slot = missing_slots[0]

        return {
            "completed": False,
            "message": QUESTIONS[next_slot]
        }

    return {
        "completed": True
    }
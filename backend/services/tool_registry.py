# backend/services/tool_registry.py

from backend.tools.appointment_tools import (
    fetch_slots,
    book_appointment,
    retrieve_appointments,
    cancel_appointment,
    modify_appointment
)

from backend.tools.user_tools import (
    identify_user,
    end_conversation
)


TOOLS = {

    "fetch_slots": fetch_slots,

    "book_appointment": book_appointment,

    "retrieve_appointments": retrieve_appointments,

    "cancel_appointment": cancel_appointment,

    "modify_appointment": modify_appointment,

    "identify_user": identify_user,

    "end_conversation": end_conversation
}
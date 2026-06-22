# backend/services/agent.py

import json
import time

from backend.services.llm import chat_with_llm
from backend.services.prompts import SYSTEM_PROMPT
from backend.services.schemas import AgentResponse
from backend.services.memory import add_message, get_history
from backend.services.session import get_state, update_state, clear_state
from backend.services.slot_manager import get_missing_slots, QUESTIONS
from backend.services.tool_executor import execute_tool
from backend.services.summarizer import generate_summary


def process_query(session_id: str, user_message: str) -> dict:
    """
    Main agent orchestration pipeline.

    Steps:
        1. Add user message to memory
        2. Build LLM messages with history
        3. Call LLM to extract intent + entities
        4. Parse structured response
        5. Update session state
        6. Check for missing slots
        7. Execute tool if slots complete
        8. Return response
    """

    start_time = time.time()

    # Track tool calls for UI
    tool_calls = []

    # 1. Add user message to memory
    add_message(session_id, "user", user_message)

    # 2. Build messages for LLM
    history = get_history(session_id)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)

    # 3. Call LLM
    try:
        raw_response = chat_with_llm(messages)
    except Exception as e:
        return {
            "message": "I'm sorry, I'm having trouble processing your request right now. Please try again.",
            "tool_calls": [],
            "latency": round(time.time() - start_time, 3)
        }

    # 4. Parse structured response
    try:
        # Clean response - remove markdown code fences if present
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()

        parsed_data = json.loads(cleaned)
        parsed = AgentResponse(**parsed_data)
    except (json.JSONDecodeError, Exception):
        # LLM didn't return valid JSON — treat raw response as conversational
        add_message(session_id, "assistant", raw_response)
        return {
            "message": raw_response,
            "tool_calls": [],
            "latency": round(time.time() - start_time, 3)
        }

    # 5. Update session state with extracted entities
    state = get_state(session_id)
    update_state(session_id, parsed.model_dump())
    state = get_state(session_id)

    intent = parsed.intent
    response_text = parsed.response

    # 6. Handle end_conversation
    if intent == "end_conversation":
        tool_calls.append({"tool": "end_conversation", "status": "generating_summary"})

        summary = ""
        try:
            summary = generate_summary(history)
        except Exception:
            summary = "Unable to generate summary."

        clear_state(session_id)

        farewell = response_text or "Thank you for visiting! Here is your conversation summary."
        add_message(session_id, "assistant", farewell)

        return {
            "message": farewell,
            "summary": summary,
            "tool_calls": tool_calls,
            "latency": round(time.time() - start_time, 3)
        }

    # 7. If we have an intent, check for missing slots
    if intent and intent != "fetch_slots":
        missing = get_missing_slots(intent, state)

        if missing:
            question = QUESTIONS.get(missing[0], "Could you provide more details?")
            msg = response_text or question
            add_message(session_id, "assistant", msg)

            tool_calls.append({
                "tool": intent,
                "status": "waiting_for_info",
                "missing": missing
            })

            return {
                "message": msg,
                "tool_calls": tool_calls,
                "latency": round(time.time() - start_time, 3)
            }

    # 8. Execute tool if intent is present and slots are complete
    if intent:
        tool_calls.append({"tool": intent, "status": "executing"})

        result = execute_tool(intent, state)

        tool_calls[-1]["status"] = "completed" if result.get("success") else "failed"
        tool_calls[-1]["result"] = result.get("message", "")

        # Build response message
        if result.get("success"):
            msg = response_text or result.get("message", "Done.")

            # Append slot details for booking confirmations
            if intent == "book_appointment":
                msg = f"{msg}\n\nAppointment confirmed for {state.get('name', 'you')} on {state.get('date')} at {state.get('time')}."

            # Append slots for fetch_slots
            if intent == "fetch_slots" and "slots" in result:
                slots_list = ", ".join(result["slots"])
                msg = f"{msg}\n\nAvailable slots: {slots_list}"

            # Append appointments list for retrieve
            if intent == "retrieve_appointments" and "appointments" in result:
                appts = result["appointments"]
                if appts:
                    appt_lines = []
                    for a in appts:
                        appt_lines.append(f"  - {a['date']} at {a['time']} ({a['name']})")
                    msg = f"{msg}\n\nYour appointments:\n" + "\n".join(appt_lines)

        else:
            msg = response_text or result.get("message", "Sorry, something went wrong.")

        add_message(session_id, "assistant", msg)

        return {
            "message": msg,
            "tool_calls": tool_calls,
            "latency": round(time.time() - start_time, 3)
        }

    # 9. No intent — just a conversational response
    msg = response_text or "I'm here to help you with appointment booking. How can I assist you today?"
    add_message(session_id, "assistant", msg)

    return {
        "message": msg,
        "tool_calls": tool_calls,
        "latency": round(time.time() - start_time, 3)
    }
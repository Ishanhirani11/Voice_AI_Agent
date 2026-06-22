# backend/services/tool_executor.py

from backend.services.tool_registry import TOOLS


def execute_tool(
        intent: str,
        state: dict
) -> dict:
    """
    Execute a tool based on intent and current session state.
    Returns a dict with 'success' and 'message' keys.
    """

    try:

        if intent == "fetch_slots":

            result = TOOLS[intent]()

        elif intent == "book_appointment":

            result = TOOLS[intent](
                state.get("name", ""),
                state.get("phone", ""),
                state.get("date", ""),
                state.get("time", "")
            )

        elif intent == "retrieve_appointments":

            result = TOOLS[intent](
                state.get("phone", "")
            )

        elif intent == "cancel_appointment":

            result = TOOLS[intent](
                state.get("phone", ""),
                state.get("date", ""),
                state.get("time", "")
            )

        elif intent == "modify_appointment":

            result = TOOLS[intent](
                state.get("phone", ""),
                state.get("old_date", ""),
                state.get("old_time", ""),
                state.get("new_date", ""),
                state.get("new_time", "")
            )

        elif intent == "identify_user":

            result = TOOLS[intent](
                state.get("name", ""),
                state.get("phone", "")
            )

        elif intent == "end_conversation":

            result = TOOLS[intent]()

        else:

            result = {
                "success": False,
                "message": f"Unknown action: {intent}"
            }

        # Guarantee dictionary output
        if not isinstance(result, dict):
            return {
                "success": False,
                "message": "Tool returned invalid output."
            }

        return result

    except KeyError as e:
        return {
            "success": False,
            "message": f"Missing required information: {str(e)}"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Tool execution failed: {str(e)}"
        }
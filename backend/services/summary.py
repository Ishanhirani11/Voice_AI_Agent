conversation_summaries = {}


def save_summary(session_id, summary):

    conversation_summaries[session_id] = summary


def get_summary(session_id):

    return conversation_summaries.get(
        session_id,
        ""
    )


def clear_summary(session_id):

    conversation_summaries[session_id] = ""
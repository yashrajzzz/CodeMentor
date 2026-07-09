from agents.agent import agent
from services.chat_history import chat_history


def ask(question, session_state):
    """
    session_state: the same per-user dict used in explanation_service.explain,
    passed in via gr.State so each user's "previously analyzed code" stays
    isolated from other concurrent users.
    """

    prompt = f"""
Previously analyzed code:

{session_state.get("last_code", "")}

Programming Language:
{session_state.get("last_language", "")}

User Level:
{session_state.get("last_level", "")}

The user now asks:

{question}

Answer ONLY based on the previously analyzed code.
"""

    chat_history.add_user_message(prompt)

    response = agent.invoke(
        {
            "messages": chat_history.messages
        }
    )

    chat_history.add_ai_message(
        response["messages"][-1].content
    )

    return response["messages"][-1].content
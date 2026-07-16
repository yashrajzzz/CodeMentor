import logging

from services.chat_history import chat_history
from services.explanation_service import _invoke_agent, TransientAgentError, ERROR_PREFIX

logger = logging.getLogger("codementor.followup_service")

MAX_QUESTION_LENGTH = 2000


def ask(question, session_state):
    """
    session_state: the same per-user dict used in explanation_service.explain.
    Appends each Q&A pair to session_state["qa_log"] so the download-report
    feature can include the full follow-up conversation.
    """

    if not question or not question.strip():
        return "⚠️ Please type a question first.", session_state

    if len(question) > MAX_QUESTION_LENGTH:
        return (
            f"⚠️ That question is a bit long ({len(question)} characters, "
            f"limit is {MAX_QUESTION_LENGTH}). Try shortening it.",
            session_state,
        )

    if not session_state.get("last_code"):
        return (
            "⚠️ I don't have any analyzed code yet — please analyze a snippet "
            "first, then ask follow-up questions about it.",
            session_state,
        )

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

    try:
        chat_history.add_user_message(prompt)

        response = _invoke_agent(chat_history.messages)
        answer = response["messages"][-1].content

        chat_history.add_ai_message(answer)

        qa_log = session_state.get("qa_log", [])
        qa_log.append({"question": question, "answer": answer})
        session_state["qa_log"] = qa_log

        return answer, session_state

    except TransientAgentError as e:
        logger.error("Agent unavailable after retries: %s", e)
        return (
            f"{ERROR_PREFIX} The AI service is temporarily unavailable after "
            f"several retries. Please try again in a moment.",
            session_state,
        )
    except Exception as e:
        logger.exception("Unexpected error in ask()")
        return f"{ERROR_PREFIX} Something went wrong answering your question: {str(e)}", session_state
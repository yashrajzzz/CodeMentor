import logging

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from agents.agent import agent

logger = logging.getLogger("codementor.explanation_service")

# Sentinel prefix so app.py can reliably detect a failure and skip markdown
# parsing entirely, instead of feeding a broken response into parse_response()
# and showing blank/garbled panels.
ERROR_PREFIX = "__CODEMENTOR_ERROR__"

MAX_CODE_LENGTH = 12000  # ~ a few thousand tokens; keeps requests within
                          # reasonable model context and avoids silent
                          # truncation failures on very large pastes


class TransientAgentError(Exception):
    """Raised for errors worth retrying (timeouts, rate limits, connection drops)."""


def _is_transient(exc: Exception) -> bool:
    text = str(exc).lower()
    transient_markers = (
        "timeout", "timed out", "rate limit", "429",
        "connection", "temporarily unavailable", "503", "502",
    )
    return any(marker in text for marker in transient_markers)


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type(TransientAgentError),
)
def _invoke_agent(messages):
    try:
        return agent.invoke({"messages": messages})
    except Exception as exc:
        if _is_transient(exc):
            logger.warning("Transient agent error, will retry: %s", exc)
            raise TransientAgentError(str(exc)) from exc
        raise


def explain(code, level, mode, language, session_state):
    """
    session_state: a per-user dict (backed by gr.State in app.py) holding
    the last analyzed code/level/mode/language, so concurrent Gradio users
    don't share or overwrite each other's context.
    """

    if code and len(code) > MAX_CODE_LENGTH:
        return (
            f"{ERROR_PREFIX} That snippet is too long ({len(code)} characters, "
            f"limit is {MAX_CODE_LENGTH}). Try analyzing a smaller section at a time.",
            session_state,
        )

    session_state["last_code"] = code
    session_state["last_level"] = level
    session_state["last_mode"] = mode
    session_state["last_language"] = language
    session_state["qa_log"] = []  # new analysis -> start a fresh follow-up log

    prompt = f"""
    User Level: {level}

    Mode: {mode}

    Programming Language: {language}

    Code:

    {code}
    """

    try:
        from services.chat_history import chat_history

        chat_history.add_user_message(prompt)

        response = _invoke_agent(chat_history.messages)

        answer = response["messages"][-1].content
        chat_history.add_ai_message(answer)

        return answer, session_state

    except TransientAgentError as e:
        logger.error("Agent unavailable after retries: %s", e)
        return (
            f"{ERROR_PREFIX} The AI service is temporarily unavailable after "
            f"several retries. Please try again in a moment.",
            session_state,
        )
    except Exception as e:
        logger.exception("Unexpected error in explain()")
        return f"{ERROR_PREFIX} Something went wrong while analyzing your code: {str(e)}", session_state
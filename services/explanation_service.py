from agents.agent import agent
from services.language_detector import detect_language

from services import session

def explain(code, level, mode, language):

    session.last_code = code
    session.last_level = level
    session.last_mode = mode
    session.last_language = language

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

        response = agent.invoke(
            {
                "messages": chat_history.messages
            }
        )

        chat_history.add_ai_message(
            response["messages"][-1].content
        )

        return response["messages"][-1].content
    except Exception as e:
        return f"Error: {str(e)}"
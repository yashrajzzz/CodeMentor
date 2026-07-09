from agents.agent import agent


def explain(code, level, mode, language, session_state):
    """
    session_state: a per-user dict (backed by gr.State in app.py) holding
    the last analyzed code/level/mode/language, so concurrent Gradio users
    don't share or overwrite each other's context.
    """

    session_state["last_code"] = code
    session_state["last_level"] = level
    session_state["last_mode"] = mode
    session_state["last_language"] = language

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

        return response["messages"][-1].content, session_state
    except Exception as e:
        return f"Error: {str(e)}", session_state
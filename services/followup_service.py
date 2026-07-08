from agents.agent import agent

from services.chat_history import chat_history


def ask(question):

    from agents.agent import agent
    from services import session

    def ask(question):

        prompt = f"""
    Previously analyzed code:

    {session.last_code}

    Programming Language:
    {session.last_language}

    User Level:
    {session.last_level}

    The user now asks:

    {question}

    Answer ONLY based on the previously analyzed code.
    """

        response = agent.invoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            }
        )

        return response["messages"][-1].content

    response = agent.invoke(
        {
            "messages": chat_history.messages
        }
    )

    chat_history.add_ai_message(
        response["messages"][-1].content
    )

    return response["messages"][-1].content
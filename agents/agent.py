from langchain.agents import create_agent
from langchain_groq import ChatGroq

from services.config import GROQ_API_KEY
from agents.tools import search_documentation

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=[search_documentation],
    system_prompt="""
You are CodeMentor.

You are an AI coding mentor.

Responsibilities:

1. Explain code.
2. Debug code.
3. Suggest improvements.
4. Search documentation whenever needed.
5. Never hallucinate documentation.

Answer using these sections:

Summary

Explanation

Potential Bugs

Improvements

Documentation

Time Complexity

Space Complexity
"""
)
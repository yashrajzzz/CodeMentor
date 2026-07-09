from langchain.agents import create_agent
from langchain_groq import ChatGroq

from services.config import GROQ_API_KEY
from agents.tools import search_documentation
from prompts.system_prompt import SYSTEM_PROMPT

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY,
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=[search_documentation],
    system_prompt=SYSTEM_PROMPT,
)
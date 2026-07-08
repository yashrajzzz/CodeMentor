from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

@tool
def search_documentation(query: str) -> str:
    """
    Search the web for official programming language documentation,
    library references, API documentation, and framework guides.
    """
    query = (
        f"{query} "
        "site:docs.python.org OR "
        "site:cppreference.com OR "
        "site:developer.mozilla.org OR "
        "site:docs.oracle.com"
    )

    return search.run(query)
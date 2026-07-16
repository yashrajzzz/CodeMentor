import logging

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

logger = logging.getLogger("codementor.tools")

search = DuckDuckGoSearchRun()


@tool
def search_documentation(query: str) -> str:
    """
    Search the web for official programming language documentation,
    library references, API documentation, and framework guides.
    """
    full_query = (
        f"{query} "
        "site:docs.python.org OR "
        "site:cppreference.com OR "
        "site:developer.mozilla.org OR "
        "site:docs.oracle.com"
    )

    try:
        return search.run(full_query)
    except Exception as e:
        logger.warning("Documentation search failed for %r: %s", query, e)
        return (
            "Documentation search is temporarily unavailable. "
            "Answer using your own knowledge and clearly note that "
            "this was not verified against live documentation."
        )
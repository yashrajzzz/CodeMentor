import re


def _normalize_markdown(text: str) -> str:
    """
    The model sometimes indents plain bullet text with 4+ leading spaces,
    which Markdown interprets as a code block. This strips accidental
    leading indentation line-by-line, while leaving the *content* of real
    ``` fenced code blocks untouched.
    """

    lines = text.split("\n")
    normalized = []
    in_fence = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            normalized.append(stripped)
            continue

        if in_fence:
            normalized.append(line)
        else:
            normalized.append(stripped)

    return "\n".join(normalized).strip()


def parse_response(response: str):

    sections = {}

    pattern = r"## (.+?)(?=\n## |\Z)"

    matches = re.findall(
        pattern,
        response,
        re.DOTALL
    )

    for match in matches:

        lines = match.split("\n", 1)

        title = lines[0].strip()

        content = ""

        if len(lines) > 1:
            content = _normalize_markdown(lines[1])

        sections[title] = content

    time_complexity = sections.get("Time Complexity", "")
    space_complexity = sections.get("Space Complexity", "")

    complexity = (
        f"**⏱️ Time Complexity**\n\n{time_complexity}\n\n"
        f"**📦 Space Complexity**\n\n{space_complexity}"
    )

    return (
        sections.get("Summary", ""),
        sections.get("Explanation", ""),
        sections.get("Analogy", ""),
        sections.get("Potential Bugs", ""),
        sections.get("Improvements", ""),
        sections.get("Documentation", ""),
        complexity,
    )
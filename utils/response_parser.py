import re

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
            content = lines[1].strip()

        sections[title] = content

    return (
        sections.get("Summary", ""),
        sections.get("Explanation", ""),
        sections.get("Analogy", ""),
        sections.get("Potential Bugs", ""),
        sections.get("Improvements", ""),
        sections.get("Documentation", ""),
        f"""Time Complexity

        {sections.get("Time Complexity","")}

        Space Complexity

        {sections.get("Space Complexity","")}
        """
    )
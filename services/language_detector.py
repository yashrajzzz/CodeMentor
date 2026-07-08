import re

def detect_language(code: str):

    code = code.lower()

    # ---------- Python ----------
    if (
        "def " in code
        or "import " in code
        or "print(" in code
        or "async def" in code
        or "lambda " in code
    ):
        return "Python"

    # ---------- C++ ----------
    cpp_keywords = [
        "#include",
        "using namespace std",
        "cout",
        "cin",
        "vector<",
        "std::",
        "int main",
        "namespace std",
        "endl",
        "->",
    ]

    if any(keyword in code for keyword in cpp_keywords):
        return "C++"

    # ---------- Java ----------
    java_keywords = [
        "public class",
        "public static void main",
        "system.out.println",
        "scanner",
    ]

    if any(keyword in code for keyword in java_keywords):
        return "Java"

    # ---------- JavaScript ----------
    js_keywords = [
        "console.log",
        "function ",
        "=>",
        "let ",
        "const ",
        "var ",
    ]

    if any(keyword in code for keyword in js_keywords):
        return "JavaScript"

    return "Unknown"
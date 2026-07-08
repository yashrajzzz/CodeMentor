import gradio as gr

from services.explanation_service import explain
from utils.response_parser import parse_response
from utils.validator import validate_input
from services.language_detector import detect_language
from services.followup_service import ask
from services import session

def analyze(code, level, mode, language, progress=gr.Progress()):

    progress(0.2, desc="Validating input...")

    if not validate_input(code):
        return (
            "Please paste some code.",
            "Please paste some code.",
            "Please paste some code.",
            "Please paste some code.",
            "Please paste some code.",
            "Please paste some code."
        )

    progress(0.5, desc="Detecting language...")

    if language == "Auto Detect":
        language = detect_language(code)

    if language == "Unknown":
        return (
            "Could not detect the programming language.\nPlease select it manually.",
            "",
            "",
            "",
            "",
            "",
        )

    progress(0.7, desc="Analyzing code...")

    response = explain(code, level, mode, language)

    progress(1.0, desc="Done!")

    summary, explanation, analogy, bugs, improvements, docs, complexity = parse_response(response)

    return (
    summary,
    explanation,
    analogy,
    bugs,
    improvements,
    docs,
    complexity,
)

def clear_chat():

    session.last_code = ""
    session.last_level = ""
    session.last_mode = ""
    session.last_language = ""

    return (
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    )

with gr.Blocks(title="CodeMentor") as demo:

    gr.Markdown("""
    # 💻 CodeMentor

    ### 🚀 AI-Powered Code Explanation & Debugging Assistant

    Explain • Debug • Learn • Improve
    """)

    with gr.Row():

        mode = gr.Radio(
            ["Explain", "Debug"],
            value="Explain",
            label="Mode"
        )

        language = gr.Dropdown(
            ["Auto Detect", "C++", "Python", "Java", "JavaScript"],
            value="Auto Detect",
            label="Language"
        )

        level = gr.Radio(
            ["Beginner", "Intermediate", "Expert"],
            value="Beginner",
            label="Explanation Level"
        )

    code = gr.Code(
        label="Paste your code"
    )
    
    gr.Markdown("### 📌 Try these examples")

    gr.Examples(
        examples=[
            [
    """def factorial(n):
        if n == 0:
            return 1
        return n * factorial(n-1)
    """
            ],

            [
    """#include<iostream>
    using namespace std;

    int main() {
        int a[5];
        cout << a[10];
    }
    """
            ],

            [
    """import requests

    requests.get(url, timeout=5)
    """
            ]
        ],
        inputs=code
    )

    

    btn = gr.Button("🚀 Analyze", variant="primary")

    with gr.Row():

        with gr.Column():

            with gr.Accordion("📝 Summary", open=True):
                summary = gr.Textbox(
                    lines=6,
                    interactive=False
                )

            with gr.Accordion("🐞 Potential Bugs", open=False):
                bugs = gr.Textbox(
                    lines=7,
                    interactive=False
                )

            with gr.Accordion("📚 Documentation", open=False):
                docs = gr.Textbox(
                    lines=8,
                    interactive=False
                )

        with gr.Column():

            with gr.Accordion("📖 Explanation", open=True):
                breakdown = gr.Textbox(
                    lines=12,
                    interactive=False
                )

            with gr.Accordion("💡 Improvements", open=False):
                improvements = gr.Textbox(
                    lines=7,
                    interactive=False
                )

            with gr.Accordion("📊 Complexity", open=False):
                complexity = gr.Textbox(
                    lines=8,
                    interactive=False
                )

    with gr.Accordion("🌍 Real World Analogy", open=False):
        analogy = gr.Textbox(
            lines=6,
            interactive=False
        )

    btn.click(
        analyze,
        [code, level, mode, language],
        [
            summary,
            breakdown,
            analogy,
            bugs,
            improvements,
            docs,
            complexity
        ]
    )

    gr.Markdown("## 💬 Follow-up Questions")

    followup = gr.Textbox(
        label="Ask anything about the previously analyzed code",
        placeholder="Example: Why is line 5 needed?"
    )

    followup_btn = gr.Button("Ask")

    followup_answer = gr.Textbox(
        label="AI Response",
        lines=8,
        interactive=False
    )

    followup_btn.click(
        ask,
        inputs=followup,
        outputs=followup_answer
    )

    clear_btn = gr.Button("🗑 Clear Chat")

    clear_btn.click(
        clear_chat,
        outputs=[
            summary,
            breakdown,
            analogy,
            bugs,
            improvements,
            docs,
            complexity,
            followup,
            followup_answer
        ]
    )

    gr.Markdown(
    """
    ---

    Built with ❤️ 
    """
    )

import os

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)
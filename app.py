import os

import gradio as gr

from services.explanation_service import explain, ERROR_PREFIX
from utils.response_parser import parse_response
from utils.validator import validate_input
from services.language_detector import detect_language
from services.followup_service import ask
from services.report_service import generate_report_file


CUSTOM_CSS = """
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}
#header-block {
    text-align: center;
    padding: 12px 0 4px 0;
}
#header-block h1 {
    font-size: 2.1rem;
    margin-bottom: 0.2rem;
}
#detected-lang {
    text-align: center;
    font-weight: 600;
}
.result-panel {
    border-radius: 14px !important;
    border: 1px solid var(--border-color-primary) !important;
    padding: 14px !important;
    background: var(--background-fill-secondary) !important;
}
#analyze-btn, #ask-btn, #download-btn {
    font-size: 1.05rem !important;
    border-radius: 10px !important;
}
footer {visibility: hidden}
"""

THEME = gr.themes.Soft(
    primary_hue="violet",
    secondary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui"],
).set(
    button_large_radius="10px",
    block_radius="14px",
)


def _empty_session():
    return {
        "last_code": "",
        "last_level": "",
        "last_mode": "",
        "last_language": "",
        "qa_log": [],
    }


def analyze(code, level, mode, session_state, progress=gr.Progress()):

    progress(0.2, desc="Validating input...")

    if not validate_input(code):
        msg = "⚠️ Please paste some code first (or it may be too long — keep it under ~12,000 characters)."
        return (
            msg, msg, msg, msg, msg, msg, msg,
            "—",
            session_state,
        )

    progress(0.4, desc="Detecting language...")

    language = detect_language(code)

    if language == "Unknown":
        msg = "🤔 Couldn't confidently detect the programming language for this snippet."
        return (
            msg, "", "", "", "", "", "",
            "Unknown",
            session_state,
        )

    progress(0.7, desc="Analyzing code...")

    response, session_state = explain(code, level, mode, language, session_state)

    progress(1.0, desc="Done!")

    # Reliability: if explain() hit a real error, don't feed the raw error
    # string into the markdown-section parser — show it cleanly instead.
    if response.startswith(ERROR_PREFIX):
        error_msg = response.replace(ERROR_PREFIX, "").strip()
        return (
            f"❌ {error_msg}",
            "", "", "", "", "", "",
            f"🔍 Detected language: **{language}**",
            session_state,
        )

    summary, explanation, analogy, bugs, improvements, docs, complexity = parse_response(response)

    return (
        summary,
        explanation,
        analogy,
        bugs,
        improvements,
        docs,
        complexity,
        f"🔍 Detected language: **{language}**",
        session_state,
    )


def ask_followup(question, session_state):
    answer, session_state = ask(question, session_state)

    if answer.startswith(ERROR_PREFIX):
        answer = f"❌ {answer.replace(ERROR_PREFIX, '').strip()}"

    return answer, session_state


def download_report(session_state, summary, explanation, analogy, bugs, improvements, docs, complexity):
    if not session_state.get("last_code"):
        gr.Warning("Analyze some code first — there's nothing to include in a report yet.")
        return None

    filepath = generate_report_file(
        session_state, summary, explanation, analogy, bugs, improvements, docs, complexity
    )
    return filepath


def clear_chat():
    return (
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "—",
        "",
        "",
        None,
        _empty_session(),
    )


with gr.Blocks(title="CodeMentor", theme=THEME, css=CUSTOM_CSS) as demo:

    # per-user session state (isolated across concurrent Gradio users)
    session_state = gr.State(_empty_session())

    with gr.Column(elem_id="header-block"):
        gr.Markdown("""
        # 💻 CodeMentor
        ### 🚀 AI-Powered Code Explanation & Debugging Assistant
        Explain • Debug • Learn • Improve — powered by AI 🤖
        """)

    with gr.Row():

        mode = gr.Radio(
            ["Explain", "Debug"],
            value="Explain",
            label="🎯 Mode"
        )

        level = gr.Radio(
            ["Beginner", "Intermediate", "Expert"],
            value="Beginner",
            label="🎓 Explanation Level"
        )

    code = gr.Code(
        label="📄 Paste your code (language is auto-detected — no need to pick it)"
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

    btn = gr.Button("🚀 Analyze Code", variant="primary", elem_id="analyze-btn")

    detected_language = gr.Markdown("—", elem_id="detected-lang")

    with gr.Row():

        with gr.Column():

            with gr.Accordion("📝 Summary", open=True):
                summary = gr.Markdown(elem_classes="result-panel")

            with gr.Accordion("🐞 Potential Bugs", open=False):
                bugs = gr.Markdown(elem_classes="result-panel")

            with gr.Accordion("📚 Documentation", open=False):
                docs = gr.Markdown(elem_classes="result-panel")

        with gr.Column():

            with gr.Accordion("📖 Explanation", open=True):
                breakdown = gr.Markdown(elem_classes="result-panel")

            with gr.Accordion("💡 Improvements", open=False):
                improvements = gr.Markdown(elem_classes="result-panel")

            with gr.Accordion("📊 Complexity", open=False):
                complexity = gr.Markdown(elem_classes="result-panel")

    with gr.Accordion("🌍 Real World Analogy", open=False):
        analogy = gr.Markdown(elem_classes="result-panel")

    btn.click(
        analyze,
        [code, level, mode, session_state],
        [
            summary,
            breakdown,
            analogy,
            bugs,
            improvements,
            docs,
            complexity,
            detected_language,
            session_state,
        ]
    )

    gr.Markdown("---\n## 💬 Follow-up Questions")

    followup = gr.Textbox(
        label="Ask anything about the previously analyzed code",
        placeholder="Example: Why is line 5 needed?"
    )

    followup_btn = gr.Button("🙋 Ask", elem_id="ask-btn")

    followup_answer = gr.Markdown(elem_classes="result-panel")

    followup_btn.click(
        ask_followup,
        inputs=[followup, session_state],
        outputs=[followup_answer, session_state]
    )

    gr.Markdown("---\n## 📥 Download Report")
    gr.Markdown("Get the full analysis plus every follow-up question and answer as a Markdown file.")

    download_btn = gr.Button("📥 Download Full Report", elem_id="download-btn")
    report_file = gr.File(label="Your report", interactive=False)

    download_btn.click(
        download_report,
        inputs=[session_state, summary, breakdown, analogy, bugs, improvements, docs, complexity],
        outputs=report_file
    )

    clear_btn = gr.Button("🗑️ Clear Chat")

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
            detected_language,
            followup,
            followup_answer,
            report_file,
            session_state,
        ]
    )

    gr.Markdown(
    """
    ---
    Built with ❤️ 
    """
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )
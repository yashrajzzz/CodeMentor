import gradio as gr

with gr.Blocks(title="CodeMentor") as demo:

    gr.Markdown("# 💻 CodeMentor")

    code = gr.Code(
        label="Paste your code"
    )

    level = gr.Radio(
        ["Beginner", "Intermediate", "Expert"],
        value="Beginner",
        label="Explanation Level"
    )

    mode = gr.Radio(
        ["Explain", "Debug"],
        value="Explain",
        label="Mode"
    )

    btn = gr.Button("Analyze")

    output = gr.Textbox(lines=15)

    btn.click(
        lambda c, l, m: f"Mode={m}\nLevel={l}",
        [code, level, mode],
        output
    )

demo.launch()
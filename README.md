---
title: CodeMentor
emoji: 💻
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 5.38.0
app_file: app.py
pinned: false
---

# 💻 CodeMentor

> AI-Powered Code Explanation & Debugging Assistant

CodeMentor is an AI-powered programming mentor that helps developers understand, debug, and improve code using Large Language Models (LLMs).

---

## ✨ Features

- Explain code for Beginner, Intermediate and Expert developers
- Debug syntax and logical errors
- Suggest code improvements
- Search official documentation
- Follow-up questions without repasting code
- Auto language detection
- Multi-language support

---

## 🛠 Tech Stack

- Python
- Gradio
- LangChain
- Groq API
- DuckDuckGo Search
- Llama 3 / GPT-OSS (via Groq)

---

## ⚙️ Setup (local)

```bash
git clone <your-repo-url>
cd CodeMentor

pip install -r requirements.txt

# create a .env file with:
# GROQ_API_KEY=your_key_here

python app.py
```

On Hugging Face Spaces, set `GROQ_API_KEY` under **Settings → Repository secrets** instead of using a `.env` file.

---

## 📂 Project Structure

```text
CodeMentor/

agents/
prompts/
services/
utils/

app.py
requirements.txt
README.md
```

---

## 👨‍💻 Author

Yashraj
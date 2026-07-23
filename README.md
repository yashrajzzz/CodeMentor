# 💻 CodeMentor

> AI-Powered Code Explanation & Debugging Assistant

🔗 **Live demo:** [codementor-p73k.onrender.com](https://codementor-p73k.onrender.com)

*(hosted on Render's free tier - the app spins down after inactivity, so the first request after a while may take ~30-50s to wake up)*

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
git clone https://github.com/yashrajzzz/CodeMentor.git
cd CodeMentor

pip install -r requirements.txt

# create a .env file with:
# GROQ_API_KEY=your_key_here

python app.py
```

On Render, set `GROQ_API_KEY` under **Environment → Environment Variables** in your Web Service settings instead of using a `.env` file.

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

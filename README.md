# ✍️ Agentic AI Blog Writer

An intelligent **Agentic AI Blog Writer** built with **LangGraph, LangChain, Google Gemini, FastAPI, and Streamlit** that automatically researches a topic, plans content, writes SEO-friendly blog posts, reviews quality, and generates a polished final article using multiple AI agents.

---

## 🚀 Features

- 🤖 Multi-Agent workflow using LangGraph
- 🔍 AI-powered topic research
- 📝 Automatic blog outline generation
- ✨ SEO-friendly blog writing
- ✅ Content review and improvement
- 📚 Reference collection
- 💾 State management with LangGraph
- ⚡ FastAPI backend
- 🎨 Interactive Streamlit interface
- 🔄 Real-time agent execution
- 📄 Markdown blog generation
- 🧠 Google Gemini LLM integration

---

# 🏗️ Architecture

```

             User Topic
                  │
                  ▼
        Research Agent
                  │
                  ▼
         Planning Agent
                  │
                  ▼
          Writer Agent
                  │
                  ▼
          Review Agent
                  │
                  ▼
        Final Blog Output
```

---

# 🛠 Tech Stack

### AI Framework

- LangGraph
- LangChain

### LLM

- Google Gemini

### Backend

- FastAPI
- Uvicorn

### Frontend

- Streamlit

### Programming Language

- Python 3.11+

---

# 📂 Project Structure

```
Agentic-AI-Blog-Writer/
│
├── notebooks/
│   ├── 1_bwa_basic.ipynb
│   ├── 2_bwa_improved_prompting.ipynb
│   ├── 3_bwa_research.ipynb
│   ├── 4_bwa_research_fine_tuned.ipynb
│   └── 5_bwa_image.ipynb
├── app.py
├── bwa_backend.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/SajadaliAI/Agentic-AI-Blog-Writer.git
```

Go to the project directory

```bash
cd Agentic-AI-Blog-Writer
```

Create a virtual environment

### Conda

```bash
conda create -n blogwriter python=3.11
conda activate blogwriter
```

or

### venv

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=your_google_api_key
```

---

# ▶️ Run Backend

```bash
uvicorn bwa_backend:app --reload
```

Backend URL

```
http://127.0.0.1:8000
```

---

# ▶️ Run Frontend

```bash
streamlit run app.py
```

---

# 🧠 Agent Workflow

### 1️⃣ Research Agent

- Collects information
- Finds relevant facts
- Understands the topic

↓

### 2️⃣ Planner Agent

- Creates article outline
- Organizes sections
- Plans headings

↓

### 3️⃣ Writer Agent

- Writes complete article
- Generates SEO-friendly content
- Produces readable paragraphs

↓

### 4️⃣ Reviewer Agent

- Reviews grammar
- Improves clarity
- Enhances quality

↓

### 5️⃣ Final Output

- Returns polished blog article

---

# 📦 Requirements

- Python 3.11+
- Google Gemini API Key
- LangGraph
- LangChain
- FastAPI
- Streamlit

---

# 🎯 Future Improvements

- Web Search integration
- RAG support
- Image generation
- AI citations
- Export to PDF
- Export to DOCX
- WordPress publishing
- Multi-language blogs
- Memory support
- Human feedback loop

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

---

# 👨‍💻 Author

**Sajad Ali**

- AI Engineer
- Generative AI Developer
- Agentic AI Enthusiast

GitHub:
https://github.com/SajadaliAI

---

# 📄 License

This project is licensed under the MIT License.
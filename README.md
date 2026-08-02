# ✍️ Agentic AI Blog Writer

An intelligent Agentic AI Blog Writer built with **LangGraph**, **LangChain**, **Google Gemini**, **Groq**, and **Tavily Search**. The application autonomously researches a given topic, generates a well-structured blog post, and creates a relevant AI-generated image to accompany the content.

---

## 🚀 Features

* 🤖 **Agentic AI Workflow:** State machine-driven orchestration powered by LangGraph.
* 🔍 **Real-Time Web Research:** Live factual research using the Tavily Search API.
* 📝 **High-Quality Generation:** Structured blog post generation using Gemini & Groq.
* 🎯 **Enhanced Prompting:** Optimized prompt engineering for engaging and human-like writing.
* 🖼️ **AI Image Generation:** Automatic contextual image generation for blog headers.
* 🌐 **Interactive Frontend:** User-friendly UI built with Streamlit.
* ⚡ **FastAPI Backend:** High-performance RESTful API endpoints.
* 🔐 **Secure Configuration:** Environment variable management via `.env`.
* 📚 **Modular Architecture:** Clean separation of frontend, backend, and prototyping notebooks.

---

## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Orchestration & LLMs:** LangChain, LangGraph, Google Gemini, Groq
* **Tools & Search:** Tavily Search API, BeautifulSoup, Requests
* **UI & API:** Streamlit, FastAPI, Uvicorn
* **Image Processing:** Pillow

---

## 📂 Project Structure

```text
Agentic-AI-Blog-Writer/
│
├── notebooks/
│   ├── 1_bwa_basic.ipynb
│   ├── 2_bwa_improved_prompting.ipynb
│   ├── 3_bwa_research.ipynb
│   ├── 4_bwa_research_fine_tuned.ipynb
│   └── 5_bwa_image.ipynb
|
├── bwa_backend.py
├── app.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
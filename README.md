✍️ Agentic AI Blog Writer
An intelligent Agentic AI Blog Writer built with LangGraph, LangChain, Google Gemini, Groq, and Tavily Search. The application researches a topic, generates a well-structured blog post, and can create a relevant AI-generated image to accompany the content.

🚀 Features
🤖 Agentic AI workflow powered by LangGraph
🔍 Real-time web research using Tavily Search
📝 High-quality blog generation with Gemini & Groq
🎯 Improved prompting for better writing quality
🖼️ AI image generation support
🌐 Interactive Streamlit frontend
⚡ FastAPI backend
🔐 Secure API key management using .env
📚 Modular and scalable project structure
🛠️ Tech Stack
Python 3.11+
LangChain
LangGraph
Google Gemini
Groq
Tavily Search API
Streamlit
FastAPI
Uvicorn
BeautifulSoup
Requests
Pillow
📂 Project Structure
Agentic-AI-Blog-Writer/
│
├── notebooks/
│   ├── 1_bwa_basic.ipynb
│   ├── 2_bwa_improved_prompting.ipynb
│   ├── 3_bwa_research.ipynb
│   ├── 4_bwa_research_fine_tuned.ipynb
│   └── 5_bwa_image.ipynb
│
├── bwa_backend.py
├── bwa_frontend.py
├── requirements.txt
├── .env.example
├── README.md
├── .gitignore
└── assets/
    ├── demo.png
    └── architecture.png```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/SajadaliAI/Agentic-AI-Blog-Writer.git
cd Agentic-AI-Blog-Writer
Create a virtual environment
conda create -n blogwriter python=3.11 -y
Activate the environment
conda activate blogwriter
Install dependencies
pip install -r requirements.txt
🔑 Environment Variables
Create a .env file in the project root.

GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
▶️ Run the Backend
uvicorn bwa_backend:app --reload
▶️ Run the Frontend
streamlit run bwa_frontend.py
🎯 Workflow
User enters a blog topic.
Tavily searches the web for relevant information.
LangGraph orchestrates the workflow.
Gemini/Groq generates a structured blog.
AI generates a related image (optional).
The final blog is displayed in the Streamlit interface.
🤝 Contributing
Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.

📄 License
This project is licensed under the MIT License.

⭐ Support
If you found this project helpful, consider giving it a ⭐ on GitHub.

Happy Coding! 🚀
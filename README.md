# AI_Research_Agent_GenAI

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![LLM](https://img.shields.io/badge/Generative%20AI-LLM-orange)
![Status](https://img.shields.io/badge/Project-Active-green)

---

## 🌟 Overview

**AI_Research_Agent_GenAI** is a modular and extensible framework built using Python to create intelligent **AI-powered research agents**.  
This project helps automate steps in a typical research workflow:

✅ Finding information  
✅ Reading and extracting insights  
✅ Structuring and synthesizing knowledge  
✅ Generating summaries, reports, or recommendations

It is designed for students, researchers, developers, and anyone building **intelligent research assistance systems** using **Generative AI & LLMs**.

---

## 🎯 Key Features

- **Modular Agent Architecture**  
  Build custom agents with interchangeable logic, prompts, and tools.

- **Research Workflow Automation**  
  Implement workflows such as reading PDFs, summarizing, extracting insights, or generating structured notes.

- **Clean & Extendable Codebase**  
  Files are organized to help you easily add new tasks, agents, tools, or pipelines.

- **LLM‑Driven Insight Generation**  
  The system can synthesize information from various inputs — text, documents, or research material.

- **Beginner-Friendly**  
  Clear structure and simple entry points to help students understand AI workflow design.

---

## 📂 Project Structure

```
AI_Research_Agent_GenAI/
│
├── app.py                        # Main entry point
├── agents.py                     # AI Agent logic
├── tasks.py                      # Research workflows
│
├── Flexi Credit Course Generative AI Project Presentation.pdf
├── Flexi Credit Course Generative AI Project Report.pdf
│
└── (additional modules and files)
```

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python **3.9+**
- pip
- Virtual environment (recommended)

---

## 🔧 Installation

```bash
git clone https://github.com/DevanshuSawarkar/AI_Research_Agent_GenAI.git
cd AI_Research_Agent_GenAI

python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🔐 Environment Setup

If your agent requires API keys (OpenAI, Gemini, etc.), create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4.1
```

---

## ▶️ Running the Application

Run the default research agent workflow:

```bash
python app.py
```

Modify workflows inside:

- `tasks.py` → To change research tasks  
- `agents.py` → To customize agent logic  
- `app.py` → To update the main flow  

---

## 📘 Example Use Cases

### ✅ **1. Research Paper Summarization**
- Load PDF  
- Extract structured insights  
- Summarize key findings  
- Generate final conclusions  

### ✅ **2. Domain-Specific Research Assistant**
Customize prompts/logic for fields like:
- Agriculture  
- Medicine  
- Cybersecurity  
- Software Engineering  
- Business analytics  

### ✅ **3. Student Academic Assistant**
- Generate chapter summaries  
- Prepare assignment notes  
- Scan research papers  
- Create viva-ready explanations  

---

## 📈 Roadmap (Planned Enhancements)

- [ ] Add Embedding-based Search  
- [ ] Add PDF/Text corpus ingestion pipeline  
- [ ] Add Chain-of-Thought agent mode  
- [ ] Add vector database (FAISS/Chroma) integration  
- [ ] Add UI dashboard using Streamlit  
- [ ] Add voice-based research agent  

---

## 🧪 Testing

```bash
pytest -q
```

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository  
2. Create a new branch  
3. Commit your changes  
4. Push and open a PR  

---

## 📄 License

This project uses the **LICENSE** file included in the repository.

---

## 🙌 Acknowledgements

Special thanks to:
- Open-source AI community  
- LLM developers & researchers  
- Contributors of this project  

---

### ⭐ If you like this project, consider giving it a star on GitHub!  

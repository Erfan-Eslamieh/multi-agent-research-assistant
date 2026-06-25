# 🔬 Multi-Agent Research Assistant

A multi-agent RAG system built with LangGraph and Streamlit that lets you chat with scientific PDFs using an intelligent 3-agent pipeline.

---

## 🤖 How It Works

This system uses **3 specialized AI agents** working together:

1. **Retriever Agent** — Splits PDFs into chunks, creates embeddings with FAISS, and retrieves the most relevant sections based on your question
2. **Reasoner Agent** — Takes the retrieved context and generates a detailed answer using GPT-4o-mini
3. **Validator Agent** — Checks if the answer actually addresses the question, assigns a confidence score (0–100%), and triggers a retry if the answer is insufficient (up to 3 attempts)

---

## ✨ Features

### 🤖 3-Agent Pipeline (Retriever → Reasoner → Validator)
An intelligent workflow where each agent has a specific role. If the Validator finds the answer lacking, it automatically sends the question back to the Retriever for another attempt.

### 📄 PDF Upload & Viewer
Upload one or multiple PDFs and view them side-by-side with the chat. When multiple PDFs are uploaded, you can filter which ones to search in.

### 💬 Multi-Session Chat History
Chat history is saved across sessions — just like ChatGPT. Switch between previous conversations from the sidebar, start new chats, or delete old ones.

### 📋 PDF Summarization
One-click summarization of your uploaded PDF using GPT-4o-mini. The summary appears directly in the chat.

### 🔍 Confidence Scoring
Every answer comes with a confidence score and a short explanation from the Validator, so you know how reliable the response is.

### 🔄 Human-in-the-Loop Retry
When the Validator decides an answer is insufficient after 3 attempts, it asks you whether to search again or accept the current answer — keeping you in control.

### 💾 Vectorstore Caching
PDF embeddings are cached on disk using FAISS. This means the second time you load the same PDF, it's instant — no re-processing needed.

---

## 📁 Project Structure

```bash



multi-agent-research-assistant/

├── app.py                 # Streamlit UI

├── graph.py               # LangGraph workflow

├── agents/

│   ├── retriever.py       # Agent 1 — PDF retrieval

│   ├── reasoner.py        # Agent 2 — Answer generation

│   └── validator.py       # Agent 3 — Answer validation

├── utils/

│   ├── pdf_loader.py      # PDF processing & FAISS

│   └── memory.py          # Session management

└── requirements.txt

```

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| LangGraph | Multi-agent workflow orchestration |
| LangChain | RAG pipeline and prompt management |
| OpenAI GPT-4o-mini | Language model for reasoning and validation |
| FAISS | Vector storage and similarity search |
| Streamlit | Web UI |
| PyPDF | PDF parsing |

---

## 🚀 Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your API key to `.env`:

```bash
OPENAI_API_KEY=your_key_here
```

Run:
```bash
streamlit run app.py
```



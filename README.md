# 🔬 Multi-Agent Research Assistant

A multi-agent RAG system built with LangGraph and Streamlit for intelligent PDF research.

## Features
- 🤖 3-Agent pipeline (Retriever → Reasoner → Validator)
- 📄 PDF upload and viewing
- 💬 Chat history with multiple sessions
- 📋 PDF summarization
- 🔍 Confidence scoring
- 🔄 Human-in-the-loop retry
- 💾 Vectorstore caching

## Tech Stack
- LangGraph
- LangChain
- OpenAI GPT-4o-mini
- FAISS
- Streamlit

## Setup
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

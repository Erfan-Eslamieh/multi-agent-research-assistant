import streamlit as st
from dotenv import load_dotenv
from graph import build_graph
from utils.memory import get_sessions, load_session, save_session, delete_session, new_session_id

load_dotenv()

st.set_page_config(page_title="Multi-Agent Research Assistant", layout="wide")
st.title("🔬 Multi-Agent Research Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = new_session_id()
if "pdf_paths" not in st.session_state:
    st.session_state.pdf_paths = []
if "pdf_names" not in st.session_state:
    st.session_state.pdf_names = {}
if "active_pdfs" not in st.session_state:
    st.session_state.active_pdfs = []

with st.sidebar:
    st.header("💬 Chats")

    if st.button("➕ New Chat"):
        st.session_state.chat_history = []
        st.session_state.session_id = new_session_id()
        st.rerun()

    sessions = get_sessions()
    for session in sessions:
        col1, col2 = st.columns([4, 1])
        with col1:
            label = f"🗂 {session['title'][:30]}\n{session['created']}"
            if st.button(label, key=f"s_{session['id']}"):
                st.session_state.chat_history = load_session(session["id"])
                st.session_state.session_id = session["id"]
                st.rerun()
        with col2:
            if st.button("🗑", key=f"d_{session['id']}"):
                delete_session(session["id"])
                if st.session_state.session_id == session["id"]:
                    st.session_state.chat_history = []
                    st.session_state.session_id = new_session_id()
                st.rerun()

    st.divider()
    st.header("📄 Upload PDFs")
    uploaded_files = st.file_uploader(
        "Upload your PDF files",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:
        st.session_state.pdf_paths = []
        st.session_state.pdf_names = {}
        for f in uploaded_files:
            path = f"temp_{f.name}"
            with open(path, "wb") as out:
                out.write(f.read())
            st.session_state.pdf_paths.append(path)
            st.session_state.pdf_names[path] = f.name
        st.success(f"{len(st.session_state.pdf_paths)} PDF(s) loaded!")

        if len(st.session_state.pdf_paths) > 1:
            st.subheader("🔍 Filter PDFs")
            selected = st.multiselect(
                "Search in:",
                options=st.session_state.pdf_paths,
                default=st.session_state.pdf_paths,
                format_func=lambda x: st.session_state.pdf_names[x]
            )
            st.session_state.active_pdfs = selected
        else:
            st.session_state.active_pdfs = st.session_state.pdf_paths

    st.divider()

    if st.button("📋 Summarize PDF") and st.session_state.pdf_paths:
        with st.spinner("Summarizing..."):
            from utils.pdf_loader import load_pdfs
            from langchain_openai import ChatOpenAI

            docs = load_pdfs(st.session_state.pdf_paths)
            full_text = " ".join([d.page_content for d in docs])[:8000]

            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            summary = llm.invoke(f"Summarize this research paper in a clear and concise way:\n\n{full_text}")

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "📋 **Summary:**\n\n" + summary.content
            })
            save_session(st.session_state.session_id, st.session_state.chat_history)
            st.rerun()

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and "details" in msg:
            with st.expander("🔍 Details"):
                st.write(f"Retrieval attempts: {msg['details']['retrieval_count']}")
                st.write(f"Valid answer: {msg['details']['is_valid']}")
                st.write(f"**Confidence:** {msg['details']['confidence']}%")
                st.write(f"**Reason:** {msg['details']['reason']}")
                st.write(f"**Source pages:** {', '.join(msg['details']['source_pages'])}")
                st.write("**Context used:**")
                st.write(msg['details']['context'])

if st.session_state.pdf_paths:
    question = st.chat_input("Ask a question about your PDFs...")

    if question:
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Agents are working..."):
                graph = build_graph()
                result = graph.invoke({
                    "question": question,
                    "pdf_paths": st.session_state.get("active_pdfs", st.session_state.pdf_paths),
                    "context": "",
                    "answer": "",
                    "is_valid": False,
                    "confidence": 0,
                    "reason": "",
                    "retrieval_count": 0,
                    "source_pages": []
                })

            st.write(result["answer"])

            if not result["is_valid"] and result.get("retrieval_count", 0) >= 3:
                st.warning(f"⚠️ جواب کافی نبود. Confidence: {result['confidence']}%")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 دوباره جستجو کن", key=f"retry_{len(st.session_state.chat_history)}"):
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": f"[retry] {question}"
                        })
                        st.rerun()
                with col2:
                    if st.button("✅ همین کافیه", key=f"accept_{len(st.session_state.chat_history)}"):
                        pass

            with st.expander("🔍 Details"):
                st.write(f"Retrieval attempts: {result['retrieval_count']}")
                st.write(f"Valid answer: {result['is_valid']}")
                st.write(f"**Confidence:** {result['confidence']}%")
                st.write(f"**Reason:** {result['reason']}")
                st.write(f"**Source pages:** {', '.join(result['source_pages'])}")
                st.write("**Context used:**")
                st.write(result["context"])

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": result["answer"],
            "details": {
                "retrieval_count": result["retrieval_count"],
                "is_valid": result["is_valid"],
                "source_pages": result["source_pages"],
                "confidence": result["confidence"],
                "reason": result["reason"],
                "context": result["context"]
            }
        })
        save_session(st.session_state.session_id, st.session_state.chat_history)
else:
    st.info("👈 Please upload PDF files from the sidebar to get started.")
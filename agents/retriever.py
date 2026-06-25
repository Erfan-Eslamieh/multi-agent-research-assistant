from utils.pdf_loader import get_retriever

def retriever_agent(state: dict) -> dict:
    question = state["question"]
    pdf_paths = state["pdf_paths"]
    
    retriever = get_retriever(pdf_paths)
    docs = retriever.invoke(question)
    
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # صفحات منبع
    source_pages = list(set([
        f"Page {doc.metadata.get('page', '?') + 1}"
        for doc in docs
    ]))
    
    return {
        **state,
        "context": context,
        "source_pages": source_pages,
        "retrieval_count": state.get("retrieval_count", 0) + 1
    }
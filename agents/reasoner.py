from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template("""
You are a research assistant. Answer the question based on the context provided.
If the context is insufficient, say "INSUFFICIENT_CONTEXT".

Context:
{context}

Question:
{question}

Answer:
""")

def reasoner_agent(state: dict) -> dict:
    chain = prompt | llm
    
    response = chain.invoke({
        "context": state["context"],
        "question": state["question"]
    })
    
    return {
        **state,
        "answer": response.content
    }

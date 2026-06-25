from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template("""
You are a validator. Check if the answer properly addresses the question.
Reply with ONLY a JSON like this:
{{"valid": true, "confidence": 85, "reason": "short reason"}}

Question: {question}
Answer: {answer}

Result:
""")

def validator_agent(state: dict) -> dict:
    if "INSUFFICIENT_CONTEXT" in state["answer"]:
        return {**state, "is_valid": False, "confidence": 0, "reason": "Insufficient context"}

    chain = prompt | llm
    response = chain.invoke({
        "question": state["question"],
        "answer": state["answer"]
    })

    import json
    try:
        text = response.content.strip()
        data = json.loads(text)
        is_valid = data.get("valid", False)
        confidence = data.get("confidence", 0)
        reason = data.get("reason", "")
    except:
        is_valid = "true" in response.content.lower()
        confidence = 50
        reason = response.content

    return {
        **state,
        "is_valid": is_valid,
        "confidence": confidence,
        "reason": reason
    }

def should_retry(state: dict) -> str:
    if state.get("retrieval_count", 0) >= 3:
        return "end"
    return "retry" if not state["is_valid"] else "end"
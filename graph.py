from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.retriever import retriever_agent
from agents.reasoner import reasoner_agent
from agents.validator import validator_agent, should_retry

class AgentState(TypedDict):
    question: str
    pdf_paths: list
    context: str
    answer: str
    is_valid: bool
    retrieval_count: int
    source_pages: list
    confidence: int
    reason: str

def build_graph():
    graph = StateGraph(AgentState)
    
    graph.add_node("retriever", retriever_agent)
    graph.add_node("reasoner", reasoner_agent)
    graph.add_node("validator", validator_agent)
    
    graph.set_entry_point("retriever")
    graph.add_edge("retriever", "reasoner")
    graph.add_edge("reasoner", "validator")
    
    graph.add_conditional_edges(
        "validator",
        should_retry,
        {
            "retry": "retriever",
            "end": END
        }
    )
    
    return graph.compile()

import json
import os
from datetime import datetime

MEMORY_DIR = "chat_sessions"

def get_sessions() -> list:
    if not os.path.exists(MEMORY_DIR):
        return []
    sessions = []
    for f in sorted(os.listdir(MEMORY_DIR), reverse=True):
        if f.endswith(".json"):
            path = os.path.join(MEMORY_DIR, f)
            with open(path, "r") as file:
                data = json.load(file)
                sessions.append({
                    "id": f.replace(".json", ""),
                    "title": data.get("title", "Untitled"),
                    "created": data.get("created", ""),
                    "messages": data.get("messages", [])
                })
    return sessions

def load_session(session_id: str) -> list:
    path = os.path.join(MEMORY_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
            return data.get("messages", [])
    return []

def save_session(session_id: str, messages: list, title: str = ""):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    path = os.path.join(MEMORY_DIR, f"{session_id}.json")
    
    if not title and messages:
        for msg in messages:
            if msg["role"] == "user":
                title = msg["content"][:40]
                break
    
    with open(path, "w") as f:
        json.dump({
            "title": title or "Untitled",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "messages": messages
        }, f, ensure_ascii=False, indent=2)

def delete_session(session_id: str):
    path = os.path.join(MEMORY_DIR, f"{session_id}.json")
    if os.path.exists(path):
        os.remove(path)

def new_session_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# backward compatibility
def load_memory() -> list:
    return []

def save_memory(messages: list):
    pass

def clear_memory():
    pass
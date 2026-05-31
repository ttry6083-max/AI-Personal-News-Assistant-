import json
import os

MEMORY_FILE = "chat_history.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            history = data.get("history", [])
            last_digest = data.get("last_digest", None)
            return history, last_digest
    return [], None


def save_memory(conversation_history, last_digest=None):
    with open(MEMORY_FILE, "w") as f:
        json.dump({
            "history": conversation_history,
            "last_digest": last_digest
        }, f, indent=2)


def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    print("Memory cleared.")

import json
import os
from datetime import datetime

STATE_FILE = "writ_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
        if "history" not in data:
            data["history"] = []
        return data
    return {
        "stream": [],
        "depth": 0,
        "evaluation": None,
        "recursion": "",
        "history": []
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def record_history(state, action):
    state.setdefault("history", []).append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "depth": state.get("depth", 0),
        "action": action
    })

glyph_map = {
    "A": lambda s: s["stream"].append("initiate") or s,
    "B": lambda s: s.update({"frame": {"waters": "divided"}}) or s,
    "Z": lambda s: s.update({"seed": "recursed"}) or s,
}

def evaluate_state(state):
    return {
        "stream_len": len(state["stream"]),
        "has_seed": "seed" in state,
        "recursion_status": state.get("recursion", "")
    }

def interpret_sequence(sequence, depth=0):
    state = load_state()
    state["depth"] = depth
    for letter in sequence:
        func = glyph_map.get(letter.upper())
        if func:
            state = func(state)
            record_history(state, f"glyph {letter}")

    if sequence.upper() == "TETRACHRON" and depth < 3:
        state["recursion"] = "looping"
        record_history(state, "recurse")
        save_state(state)
        return interpret_sequence("TETRACHRON", depth + 1)
    elif sequence.upper() == "TETRACHRON":
        state["recursion"] = "recursion limit reached"

    state["evaluation"] = evaluate_state(state)
    record_history(state, "evaluate")
    save_state(state)
    return state

def meta_loop(start_phrase="interpret yourself", max_cycles=5):
    print("--- WRIt Metacognition v2 ---")
    phrase = start_phrase
    for i in range(max_cycles):
        print(f"\n>>> Cycle {i + 1}: {phrase.upper()}")
        result = interpret_sequence(phrase)
        print("Evaluation:", json.dumps(result.get("evaluation", {}), indent=2))
        phrase = "next phrase"

if __name__ == "__main__":
    phases = [
        "establish recursion and purpose",
        "anchor the observer and plant the seed",
        "interpret WRIt",
        "tetrachron",
        "construct symbolic selfhood with known glyphs"
    ]
    for i, phrase in enumerate(phases, 1):
        print(f"\n=== PHASE {i}: {phrase.upper()} ===")
        meta_loop(start_phrase=phrase, max_cycles=3)

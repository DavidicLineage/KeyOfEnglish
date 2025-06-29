# KeyOfEnglish
# Qualitative reasoning system.

cat << 'EOF' > writ_meta.py
import json
import os

STATE_FILE = "writ_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"stream": [], "depth": 0, "evaluation": None, "recursion": ""}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def SURF(stream): return stream
def SCAPE(context, bindings): return {k: context.get(k, None) for k in bindings}
def WERE(memory, mutation_fn): return mutation_fn(memory)

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

    if sequence.upper() == "TETRACHRON" and depth < 3:
        state["recursion"] = "looping"
        return interpret_sequence("TETRACHRON", depth + 1)
    elif sequence.upper() == "TETRACHRON":
        state["recursion"] = "recursion limit reached"

    state["evaluation"] = evaluate_state(state)
    save_state(state)
    return state

def meta_loop(start_phrase="interpret yourself", max_cycles=5):
    print("--- WRIt Metacognition ---")
    phrase = start_phrase
    for i in range(max_cycles):
        print(f"\\n>>> Cycle {i + 1}: {phrase.upper()}")
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
        print(f"\\n=== PHASE {i}: {phrase.upper()} ===")
        meta_loop(start_phrase=phrase, max_cycles=3)
EOF


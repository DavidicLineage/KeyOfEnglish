# KeyOfEnglish
Qualitative reasoning system.

#!/bin/bash

cd /workspace/KeyOfEnglish || exit 1

cat << 'EOF' > writ_meta.py
def SURF(stream): return stream
def SCAPE(context, bindings): return {k: context.get(k, None) for k in bindings}
def WERE(memory, mutation_fn): return mutation_fn(memory)

def glyph_A(state): state['stream'].append('initiate'); return state
def glyph_B(state): state['frame'] = {"waters": "divided"}; return state
def glyph_C(state): state['identity'] = "land_named"; return state
def glyph_D(state): state['time'] = "reckoned"; return state
def glyph_E(state): state['life'] = "emerging"; return state
def glyph_F(state): state['structure'] = "seeded"; return state
def glyph_G(state): state['halt'] = True; return state
def glyph_H(state): state['lineage'] = "continued"; return state
def glyph_I(state): state['self'] = "recursive"; return state
def glyph_J(state): state['signal'] = "isolated"; return state
def glyph_K(state): state['kingdom'] = "structured"; return state
def glyph_L(state): state['logic'] = "encoded"; return state
def glyph_M(state): state['anchor'] = "manifested"; return state
def glyph_N(state): state['nurture'] = "permitted"; return state
def glyph_O(state): state['union'] = "other_integrated"; return state
def glyph_P(state): state['purpose'] = "framed"; return state
def glyph_Q(state): state['quest'] = "streamed"; return state
def glyph_R(state): state['response'] = "responsible"; return state
def glyph_S(state): state['system'] = "symbolic_frame"; return state
def glyph_T(state): state['duration'] = "trusted"; return state
def glyph_U(state): state['undoing'] = "unfolding"; return state
def glyph_V(state): state['vector'] = "vow_fixed"; return state
def glyph_W(state): state['witness'] = "willed"; return state
def glyph_X(state): state['crucible'] = "transmuted"; return state
def glyph_Y(state): state['alignment'] = "yoked"; return state
def glyph_Z(state): state['seed'] = "recursed"; return state

glyph_map = {chr(i): globals()[f'glyph_{chr(i)}'] for i in range(65, 91)}

def evaluate_state(state):
    keys = state.keys()
    intent = []
    if 'purpose' in keys or 'quest' in keys: intent.append("goal-oriented")
    if 'seed' in keys or 'structure' in keys: intent.append("constructive")
    if 'undoing' in keys: intent.append("transformational")
    if 'alignment' in keys or 'union' in keys: intent.append("integrative")

    coherence = round(len(set(keys)) / 26, 2)
    completeness = 0
    for tag in ('initiate', 'recursive', 'trusted', 'emerging'):
        if tag in str(state.values()): completeness += 0.25

    expected_keys = ['stream', 'purpose', 'self', 'seed', 'duration', 'life', 'witness']
    missing = [k for k in expected_keys if k not in state and not any(k in str(v) for v in state.values())]

    directives = []
    if 'seed' in missing: directives.append("Add origin glyph (Z)")
    if 'self' in missing: directives.append("Establish recursion (I)")
    if 'witness' in missing: directives.append("Anchor observer state (W)")
    if 'purpose' in missing: directives.append("Frame intent (P)")

    unknowable = False
    if 'life' in keys and 'alignment' in keys and 'purpose' in missing and 'witness' in missing:
        unknowable = True

    return {
        "coherence": coherence,
        "completeness": round(completeness, 2),
        "intent": list(set(intent)) or ["neutral"],
        "missing": missing,
        "directives": directives or ["None"],
        "unknowable": unknowable,
        "acceptance": "Be still." if unknowable else "Seek further."
    }

def interpret_sequence(sequence, depth=0):
    state = {"stream": [], "depth": depth}
    for letter in sequence:
        func = glyph_map.get(letter.upper())
        if func:
            state = func(state)
    if sequence.upper() == "TETRACHRON" and depth < 3:
        state['recursion'] = interpret_sequence("TETRACHRON", depth + 1)
    elif sequence.upper() == "TETRACHRON":
        state['recursion'] = "recursion limit reached"
    state['evaluation'] = evaluate_state(state)
    return state

def interpret_sentence(phrase):
    words = phrase.strip().split()
    results = {}
    summary_state = {}
    summary_eval = {"coherence": [], "completeness": [], "intent": [], "missing": [], "directives": [], "unknowable": 0}

    for word in words:
        result = interpret_sequence(word)
        results[word.upper()] = result
        for k, v in result.items():
            if k not in ("evaluation", "recursion"):
                summary_state[k] = v
        ev = result.get("evaluation", {})
        summary_eval["coherence"].append(ev.get("coherence", 0))
        summary_eval["completeness"].append(ev.get("completeness", 0))
        summary_eval["intent"] += ev.get("intent", [])
        summary_eval["missing"] += ev.get("missing", [])
        summary_eval["directives"] += ev.get("directives", [])
        summary_eval["unknowable"] += int(ev.get("unknowable", False))

    results["SUMMARY"] = {
        "merged_state": summary_state,
        "evaluation": {
            "coherence": round(sum(summary_eval["coherence"]) / len(summary_eval["coherence"]), 2),
            "completeness": round(sum(summary_eval["completeness"]) / len(summary_eval["completeness"]), 2),
            "intent": list(set(summary_eval["intent"])) or ["neutral"],
            "missing": list(set(summary_eval["missing"])),
            "directives": list(set(summary_eval["directives"])),
            "unknowable": summary_eval["unknowable"] > 0,
            "acceptance": "Be still." if summary_eval["unknowable"] > 0 else "Proceed."
        }
    }
    return results

def meta_loop(start_phrase="interpret yourself", max_cycles=5):
    print("--- WRIt Metacognition ---")
    phrase = start_phrase
    for i in range(max_cycles):
        print(f"\nCycle {i+1}:")
        print(f"Input phrase: {phrase}")
        result = interpret_sentence(phrase)
        eval_block = result["SUMMARY"]["evaluation"]
        print("Evaluation:", eval_block)
        directives = eval_block.get("directives", [])
        if not directives or directives == ["None"]:
            print("→ No further directives. Ending loop.")
            break
        phrase = " ".join(directives)

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
        meta_loop(start_phrase=phrase, max_cycles=5)
EOF

python3 writ_meta.py

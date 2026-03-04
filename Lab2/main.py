from finite_automaton import FiniteAutomaton
from grammar import Grammar


ndfa = FiniteAutomaton(
    Q     = {"q0","q1","q2","q3"},
    sigma = {"a","b"},
    delta = {
        ("q0","a"): ["q1"],
        ("q0","b"): ["q0"],
        ("q1","b"): ["q1","q2"],   
        ("q2","a"): ["q2"],
        ("q2","b"): ["q3"],
    },
    q0    = "q0",
    F     = {"q3"},
)

print("=" * 60)
print("ORIGINAL FINITE AUTOMATON (Variant 16)")
print("=" * 60)
print(ndfa)

# Task 1: FA -> Regular Grammar
print("\n" + "=" * 60)
print("TASK 1 — FA converted to Regular Grammar")
print("=" * 60)
rg = ndfa.to_regular_grammar()
print(rg)
print(f"\nChomsky classification: {rg.classify_chomsky()}")

# Task 2: Determinism check
print("\n" + "=" * 60)
print("TASK 2 — Determinism check")
print("=" * 60)
det = ndfa.is_deterministic()
print(f"Is the FA deterministic? {'Yes – DFA' if det else 'No – NDFA'}")
print("Reason: δ(q1, b) = {q1, q2} → two possible targets for one (state,symbol) pair.")

# Task 3: NDFA -> DFA 
print("\n" + "=" * 60)
print("TASK 3 — Subset construction: NDFA → DFA")
print("=" * 60)
dfa = ndfa.to_dfa()
print(dfa)
print(f"\nIs resulting FA deterministic? {'Yes' if dfa.is_deterministic() else 'No'}")

# Bonus: DOT output 
print("\n" + "=" * 60)
print("BONUS — Graphviz DOT (paste at https://dreampuf.github.io/GraphvizOnline/)")
print("=" * 60)
print("\n--- NDFA ---")
print(ndfa.to_dot("NDFA"))
print("\n--- DFA ---")
print(dfa.to_dot("DFA"))

# Grammar Chomsky classification demo 
print("\n" + "=" * 60)
print("EXTRA — Grammar Chomsky classification examples")
print("=" * 60)

grammars = {
    "Type 3 (right-linear)": Grammar(
        VN={"S","A"}, VT={"a","b"}, S="S",
        P={"S":["aA","b"], "A":["bS","a"]}
    ),
    "Type 2 (context-free)": Grammar(
        VN={"S"}, VT={"a","b"}, S="S",
        P={"S":["aSb","ab"]}
    ),
    "Type 1 (context-sensitive)": Grammar(
        VN={"S","A","B"}, VT={"a","b","c"}, S="S",
        P={"S":["abc","aAbc"], "Ab":["bA"], "Ac":["Bbcc"], "bB":["Bb"], "aB":["aa"]}
    ),
}

for label, g in grammars.items():
    print(f"  {label:40s} → {g.classify_chomsky()}")

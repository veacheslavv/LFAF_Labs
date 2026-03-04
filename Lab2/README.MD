# Laboratory Work #2 - Determinism in Finite Automata, NDFA→DFA, Chomsky Hierarchy

**Course:** Formal Languages & Finite Automata
**Variant:** 16
**Student:** Morari Veaceslav
**Group:** FAF-243

---

## Objectives

1. Understand what an automaton is and what it can be used for.
2. Provide a function in the Grammar class that classifies the grammar based on the Chomsky hierarchy.
3. Implement conversion of a finite automaton to a regular grammar.
4. Determine whether the given FA is deterministic or non-deterministic.
5. Implement the conversion algorithm from NDFA to DFA.
6. Represent the finite automaton graphically (bonus).

---

## Automaton Specification

**Variant 16:**
```
Q  = {q0, q1, q2, q3}     // States
Σ  = {a, b}               // Alphabet
F  = {q3}                 // Final states
q0 = q0                   // Initial state

Transition function (δ):
    δ(q0, a) = q1
    δ(q0, b) = q0
    δ(q1, b) = q1          // same (state, symbol) — two targets → NDFA
    δ(q1, b) = q2          //
    δ(q2, a) = q2
    δ(q2, b) = q3
```

This automaton is **non-deterministic** because δ(q1, b) maps to two different states simultaneously.

---

## Implementation

### 1. Grammar Class (`grammar.py`)

Extends the Grammar class from Lab 1 with a `classify_chomsky()` method that walks the production rules and determines the grammar type. It checks for right-linear form (A → aB or A → a) and left-linear form (A → Ba or A → a) to identify Type 3, then checks single non-terminal on the left-hand side for Type 2, then compares lengths of left- and right-hand sides for Type 1, and defaults to Type 0 otherwise.

### 2. Finite Automaton Class (`finite_automaton.py`)

Stores the FA as a transition dictionary in NDFA format where each key (state, symbol) maps to a list of target states. This naturally represents both DFA (lists of length 1) and NDFA (lists of length > 1).

`to_regular_grammar()` converts the automaton to a regular grammar. Each state becomes a non-terminal, each transition δ(qi, a) = qj produces the rule qi → a qj, and an additional terminal rule qi → a is added whenever qj is a final state.

`is_deterministic()` iterates over all transition entries and returns False as soon as any (state, symbol) pair maps to more than one state.

`to_dfa()` implements the subset construction algorithm. It treats sets of NDFA states as single DFA states, performs a BFS from the start set {q0}, and at each step computes the union of all transitions reachable from the current set under each symbol. A DFA state is marked final if it contains at least one NDFA final state.

`to_dot()` returns a Graphviz DOT string for visual rendering (bonus).

### 3. Main Program (`main.py`)

Demonstrates all tasks in sequence: prints the original NDFA, converts it to a regular grammar and classifies it, checks determinism, runs the subset construction and prints the resulting DFA, and finally prints DOT strings for both automata.

---

## How to Run

**Requirements:** Python 3.8+
```bash
python3 main.py
```

**Expected output:**
1. Original NDFA structure and transitions
2. Equivalent regular grammar and its Chomsky classification
3. Determinism check result with explanation
4. Full DFA transition table after subset construction
5. Graphviz DOT strings for both NDFA and DFA (bonus)

---

## Results

### Task 1 — FA to Regular Grammar

Applying the conversion rules to Variant 16 produces the following grammar:
```
q0 → a q1  |  b q0
q1 → b q1  |  b q2
q2 → a q2  |  b q3  |  b
```

Chomsky classification: **Type 3 – Regular Grammar**

### Task 2 — Determinism Check

The transition δ(q1, b) has two targets: q1 and q2. Since a single (state, symbol) pair leads to more than one state, the automaton is **non-deterministic (NDFA)**.

### Task 3 — Subset Construction: NDFA → DFA

Each row represents a DFA super-state (a set of NDFA states) and its transitions under each input symbol.

| DFA State | a | b | Final? |
|-----------|---|---|--------|
| {q0} (start) | {q1} | {q0} | No |
| {q1} | — | {q1,q2} | No |
| {q1,q2} | {q2} | {q1,q2,q3} | No |
| {q2} | {q2} | {q3} | No |
| {q3} | — | — | **Yes** |
| {q1,q2,q3} | {q2} | {q1,q2,q3} | **Yes** |

The resulting DFA has **6 states**. Final states are any super-state that contains q3, namely {q3} and {q1,q2,q3}.

### Bonus — Graphviz Visualization

The `to_dot()` method generates a DOT string for both the NDFA and the DFA. Paste the output into [dreampuf.github.io/GraphvizOnline](https://dreampuf.github.io/GraphvizOnline) to render the diagram without installing any additional libraries.

---

## Project Structure
```
laboratory-work-2/
├── grammar.py              # Grammar class with Chomsky classifier
├── finite_automaton.py     # FiniteAutomaton class with all conversions
├── main.py                 # Main execution script
└── README.md               # This file
```

---

## Conversion Process: NDFA → DFA

The subset construction works by treating every possible *set* of NDFA states as a single DFA state. Starting from {q0}, for each input symbol the algorithm computes the union of all states reachable from every member of the current set. If that union has not been seen before, it becomes a new DFA state and is added to the processing queue. The process ends when no new sets are discovered. A DFA state is accepting if and only if at least one of its component NDFA states was accepting.

The key insight for Variant 16 is that the non-determinism at δ(q1, b) forces the creation of the super-state {q1, q2}, which then propagates into {q1, q2, q3} — a final state — once b is read again.

---

## Chomsky Hierarchy

The classifier in `grammar.py` handles all four grammar types:

| Type | Name | Rule form checked |
|------|------|-------------------|
| 3 | Regular | A → aB or A → a (right-linear), A → Ba or A → a (left-linear) |
| 2 | Context-Free | Single non-terminal on LHS |
| 1 | Context-Sensitive | \|LHS\| ≤ \|RHS\| for all productions |
| 0 | Unrestricted | No restrictions |

---

## Conclusions

1. ✅ Chomsky classifier correctly identifies right-linear grammars as Type 3 and handles all four hierarchy levels.
2. ✅ FA-to-grammar conversion produces a valid right-linear regular grammar from Variant 16.
3. ✅ The automaton is confirmed non-deterministic due to δ(q1, b) = {q1, q2}.
4. ✅ Subset construction produces a correct 6-state DFA that accepts the same language.
5. ✅ Graphviz DOT output provides visual confirmation of both automata structures.

The core takeaway is that non-determinism adds expressive convenience during modeling but not expressive power — every NDFA can always be converted to an equivalent DFA, at the cost of an exponential worst-case blowup in the number of states (though Variant 16 only grows from 4 to 6).

---

## References

Course materials: "Formal Languages & Finite Automata" by Cretu Dumitru and Vasile Drumea, Irina Cojuhari.
Hopcroft, J. E., Motwani, R., Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*. Pearson.

---

**Date:** February 2026
**Repository:** [GitHub Link]

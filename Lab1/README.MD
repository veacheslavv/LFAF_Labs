# Laboratory Work #1 - Formal Languages and Finite Automata

**Variant:** 16  
**Student:** [Morari Veaceslav]  
**Group:** [FAF-243]

---

## Task

Implement grammar and finite automaton for variant 16:

```
VN = {S, A, B}
VT = {a, b, c, d}
P = {
    S → bS
    S → dA
    A → aA
    A → dB
    A → b
    B → cB
    B → a
}
```

---

## What's Done

✅ `Grammar` class - generates strings using rules  
✅ `FiniteAutomaton` class - validates strings  
✅ Grammar to automaton conversion  
✅ Testing with examples

---

## How to Run

```bash
python3 main.py
```

**Output:**
- 5 generated strings
- Automaton structure
- Test string validation

---

## Examples

**Valid strings:**
- `db` ✓
- `dab` ✓
- `bbbdab` ✓
- `ddcca` ✓

**Invalid strings:**
- `abc` ✗ (doesn't start with b or d)
- `da` ✗ (doesn't end correctly)

---

## Project Structure

```
├── grammar.py              # Grammar class
├── finite_automaton.py     # Automaton class
├── main.py                 # Main program
└── README.md               # This file
```

---

## Automaton (transitions)

| State     | a | b | c | d |
|-----------|---|---|---|---|
| S (start) | - | S | - | A |
| A         | A | X✓| - | B |
| B         | X✓| - | B | - |

X✓ = final/accepting state

---

## Conclusions

1. Grammar successfully generates language strings
2. Automaton correctly recognizes valid strings
3. Grammar → automaton conversion works properly
4. All tests passed

---

**Date:** February 2026

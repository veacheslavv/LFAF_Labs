# Laboratory Work #1 - Formal Languages and Finite Automata

**Course:** Formal Languages & Finite Automata  
**Variant:** 16  
**Student:** Morari Veaceslav
**Group:** FAF-243

---

## Objectives

1. Understand formal language components (alphabet, grammar, productions)
2. Implement a Grammar class that generates valid strings
3. Convert Grammar to Finite Automaton
4. Implement string validation using the Finite Automaton

---

## Grammar Specification

**Variant 16:**

```
VN = {S, A, B}          // Non-terminal symbols
VT = {a, b, c, d}       // Terminal symbols
S = S                   // Start symbol

Production Rules (P):
    S → bS              // Can repeat 'b' at start
    S → dA              // Transition to state A
    A → aA              // Can repeat 'a'
    A → dB              // Transition to state B
    A → b               // Terminal production
    B → cB              // Can repeat 'c'
    B → a               // Terminal production
```

This is a **right-linear regular grammar** (Type 3 in Chomsky hierarchy).

---

## Implementation

### 1. Grammar Class (`grammar.py`)

**Features:**
- Stores grammar components (VN, VT, P, S)
- `generate_string()` - Randomly generates valid strings by applying production rules
- `to_finite_automaton()` - Converts grammar to equivalent FA

**Algorithm for string generation:**
1. Start with symbol S
2. Randomly select applicable production rule
3. Apply rule and replace non-terminal
4. Repeat until only terminals remain

### 2. Finite Automaton Class (`finite_automaton.py`)

**Features:**
- Stores FA components (Q, Σ, δ, q₀, F)
- `string_belong_to_language()` - Validates if string is accepted

**Algorithm for validation:**
1. Start from initial state q₀
2. Read each symbol and follow transitions
3. Accept if final state is reached after reading entire string

### 3. Main Program (`main.py`)

Demonstrates all functionality:
- Creates Grammar instance
- Generates 5 example strings
- Converts Grammar → FA
- Tests validation on 11 test strings

---

## How to Run

**Requirements:** Python 3.8+

```bash
# Run the program
python3 main.py
```

**Expected Output:**
1. Grammar structure display
2. 5 generated valid strings
3. Finite Automaton structure (states, transitions)
4. Validation results for test strings

---

## Results

### Generated Strings Examples

```
1. bdb
2. bdda
3. bbbdda
4. dab
5. bbbdb
```

### Automaton Structure

**States (Q):** {S, A, B, X}  
**Alphabet (Σ):** {a, b, c, d}  
**Initial State (q₀):** S  
**Final States (F):** {X}

**Transition Function (δ):**

| State     | a | b | c | d |
|-----------|---|---|---|---|
| S (start) | - | S | - | A |
| A         | A | X✓| - | B |
| B         | X✓| - | B | - |

X✓ = transition to final/accepting state

### String Validation Examples

**Accepted strings:**
- `db` ✓ - Path: S →(d) A →(b) X
- `dab` ✓ - Path: S →(d) A →(a) A →(b) X
- `bbbdab` ✓ - Path: S →(b) S →(b) S →(b) S →(d) A →(a) A →(b) X
- `ddcca` ✓ - Path: S →(d) A →(d) B →(c) B →(c) B →(a) X

**Rejected strings:**
- `abc` ✗ - No transition from S on 'a'
- `da` ✗ - State A cannot reach final state with 'a' alone
- `bdca` ✗ - State A has no transition on 'c'

---

## Project Structure

```
laboratory-work-1/
├── grammar.py              # Grammar class implementation
├── finite_automaton.py     # Finite Automaton class implementation
├── main.py                 # Main execution script
├── README.md               # This file
```

---

## Language Properties

**Accepted String Patterns:**

1. `b*da*b` - Any number of 'b's, then 'd', any number of 'a's, ending with 'b'
   - Examples: `db`, `bdab`, `daaab`, `bbbdab`

2. `b*da*dc*a` - Start with 'b's, then 'd', 'a's, 'd', 'c's, ending with 'a'
   - Examples: `dda`, `ddca`, `dadca`, `bddccca`

**Minimal String:** `db` (length = 2)

**Key Characteristics:**
- Must start with 'b' or 'd'
- Must end with 'b' or 'a' (terminal productions)
- Regular language (can be recognized by finite automaton)

---

## Conversion Process: Grammar → FA

**Conversion Rules:**
1. Each non-terminal becomes a state
2. Add one final state X
3. For rule `A → aB`: create transition δ(A, a) = B
4. For rule `A → a`: create transition δ(A, a) = X

**Example:**
- Production `S → bS` becomes δ(S, b) = S (loop)
- Production `A → b` becomes δ(A, b) = X (to final state)

---

## Conclusions

1. ✅ Successfully implemented Grammar class for Variant 16
2. ✅ String generation algorithm works correctly with recursive productions
3. ✅ Grammar to FA conversion follows standard rules
4. ✅ Finite Automaton correctly validates all test strings
5. ✅ Demonstrated equivalence between regular grammar and finite automaton

**Key Learning:**
- Regular grammars can be mechanically converted to finite automata
- Both representations describe the same language
- FA provides efficient string validation (O(n) time complexity)

---

## References

- Course materials: "Formal Languages & Finite Automata" by Cretu Dumitru
- Hopcroft, J. E., et al. (2006). Introduction to Automata Theory, Languages, and Computation

---

**Date:** February 2026  
**Repository:** [GitHub Link]

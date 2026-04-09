# Laboratory Work #4 — Regular Expressions Generator

**Course:** Formal Languages & Finite Automata
**Student:** Morari Veaceslav
**Group:** FAF-243

---

## Objectives

Understand what regular expressions are.
Learn how regular expressions can be interpreted programmatically.
Implement a generator that produces valid strings based on given regex patterns.
Simulate regex processing dynamically (not hardcoded).

---

## Theory

Regular expressions (regex) are formal patterns used to describe sets of strings over an alphabet. They are widely used in computer science for pattern matching, text processing, compilers and interpreters, and input validation.

A regular expression defines a language, meaning all strings that satisfy the pattern.

Basic regex operations include concatenation, union, Kleene star, plus, and power. Concatenation means one symbol follows another. Union represents a choice between symbols. Kleene star allows zero or more repetitions. Plus requires at least one repetition. Power represents an exact number of repetitions.

Regular expressions are closely related to finite automata, as every regex can be converted into an automaton.

---

## Given Regular Expressions (Variant 4)

### Expression 1

```
(S|T)(U|V)W*Y+24
```

### Expression 2

```
L(M|N)O^3P*Q(2|3)
```

### Expression 3

```
R*S(T|U|V)W(X|Y|Z)^2
```

---

## Interpretation

### Expression 1

The first part (S|T) means either S or T is chosen. Then (U|V) means either U or V. The symbol W with a star means it can repeat from zero up to five times due to imposed limitation. The symbol Y with plus means it repeats from one up to five times. The expression ends with the constant 24.

Example outputs:

```
SUY24
SVWWYYY24
TUYYYY24
```

---

### Expression 2

The expression starts with L. Then (M|N) means either M or N. The part O^3 means the symbol O is repeated exactly three times. The symbol P with a star allows repetition from zero to five times. Then Q is fixed. Finally, (2|3) means either 2 or 3.

Example outputs:

```
LMOOOQ2
LNOOOPPPQ3
LMOOOPQ2
```

---

### Expression 3

The symbol R with a star allows zero to five repetitions. Then S is fixed. The part (T|U|V) selects one symbol. Then W is fixed. Finally, (X|Y|Z)^2 means exactly two symbols chosen from X, Y, or Z.

Example outputs:

```
STWXX
RRRSUWYZ
RSVWXY
```

---

## Implementation

### Overview

The program dynamically parses regular expressions and generates valid strings based on them. It does not rely on hardcoded solutions but instead interprets regex patterns step by step.

---

### Token Types

| Type    | Description                 | Example       |     |
| ------- | --------------------------- | ------------- | --- |
| `CHAR`  | Single symbol               | `A`, `B`, `1` |     |
| `OR`    | Choice between symbols      | `(A           | B)` |
| `STAR`  | Zero or more repetitions    | `A*`          |     |
| `PLUS`  | One or more repetitions     | `A+`          |     |
| `POWER` | Fixed number of repetitions | `A^3`         |     |

---

### Parsing

The regex is processed character by character. Parentheses are used for grouping. The symbol | splits alternatives. The operators *, +, and ^n define repetition.

Example parsing:

```
(S|T) → OR[S, T]
W* → STAR[W]
Y+ → PLUS[Y]
```

---

### Generation Algorithm

The generation starts from an empty string. Tokens are processed sequentially. Each token expands the current set of strings. A character is appended directly. A choice creates multiple branches. Repetition expands according to limits. The results are combined step by step until full strings are formed.

---

### Example Execution

For expression:

```
(S|T)(U|V)W*Y+24
```

Processing:

```
Step 1: (S|T) → S  
Step 2: (U|V) → V  
Step 3: W* → WWW  
Step 4: Y+ → YY  
Result: SVWWWYY24
```

---

## Results

The program generates multiple valid strings for each regex.

### Expression 1 (sample)

```
SUY24
SVWWYY24
TUYYYY24
```

### Expression 2 (sample)

```
LMOOOQ2
LNOOOPPPQ3
LMOOOPQ2
```

### Expression 3 (sample)

```
STWXX
RRRSUWYZ
RSVWXY
```

---

## Limitations

Repetition operators are limited to a maximum of five to avoid extremely large outputs. Nested parentheses are not fully supported. Output size grows exponentially for complex expressions.

---

## Difficulties

Designing a parser for regex expressions was challenging. Handling repetition operators correctly required careful logic. Preventing combinatorial explosion was necessary. Maintaining dynamic behavior without hardcoding required additional structure.

---

## Conclusions

A working regex-based string generator was implemented. The program successfully interprets regex patterns dynamically. The relationship between regex and finite automata was demonstrated. The project helped understand how repetition and branching influence language size. Practical experience with parsing and generation algorithms was gained.

---

## How to Run

**Requirements:** Python 3.8+

```bash
python3 main.py
```

---

## Project Structure

```
regex-generator/
├── main.py
├── regex_parser.py
├── generator.py
├── utils.py
└── REPORT.md
```

---

## References

Cretu Dumitru, Vasile Drumea, Irina Cojuhari — course materials FLFA
Wikipedia — Regular expression: https://en.wikipedia.org/wiki/Regular_expression
GeeksforGeeks — Regular Expressions Tutorial: https://www.geeksforgeeks.org/regular-expressions/

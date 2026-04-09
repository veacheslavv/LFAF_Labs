# Regular Expressions Generator – Variant 4

## 📌 Author
Student: [Your Name]

---

## 🔹 Objective

The purpose of this project is to:
- Understand regular expressions
- Dynamically interpret regex input
- Generate valid strings based on regex rules

---

## 🔹 What are Regular Expressions?

Regular expressions (regex) are patterns used to match combinations of characters in strings.  
They are widely used in:
- Text processing
- Compilers
- Input validation
- Search algorithms

---

## 🔹 Given Regular Expressions

### 1
(S|T)(U|V)W*Y+24

### 2
L(M|N)O^3P*Q(2|3)

### 3
R*S(T|U|V)W(X|Y|Z)^2

---

## 🔹 Interpretation

### Expression 1
- (S|T): S or T
- (U|V): U or V
- W*: 0 to 5 repetitions
- Y+: 1 to 5 repetitions
- 24: constant

Example:
SUWWYYY24

---

### Expression 2
- L: constant
- (M|N): M or N
- O^3: exactly 3 times
- P*: 0–5 times
- Q: constant
- (2|3): either 2 or 3

Example:
LNOOOPPPQ3

---

### Expression 3
- R*: 0–5 times
- S: constant
- (T|U|V): one symbol
- W: constant
- (X|Y|Z)^2: exactly 2 symbols

Example:
RRRSUWYZ

---

## 🔹 Algorithm

1. Parse regex into tokens:
   - CHAR
   - OR
   - STAR (*)
   - PLUS (+)
   - POWER (^n)

2. Generate strings:
   - Concatenate step-by-step
   - Expand repetitions with limit = 5

---

## 🔹 Limitations

- `*` and `+` limited to 5 repetitions
- No nested parentheses support (basic implementation)

---

## 🔹 Difficulties

- Parsing regex dynamically
- Handling repetition operators
- Avoiding combinatorial explosion

---

## 🔹 Conclusion

The project demonstrates:
- Understanding of formal languages
- Ability to interpret regex dynamically
- Implementation of generator logic

---

## 🔹 How to Run

```bash
python main.py

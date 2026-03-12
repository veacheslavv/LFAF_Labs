# Laboratory Work #3 — Lexer & Scanner

**Course:** Formal Languages & Finite Automata
**Student:** Morari Veaceslav
**Group:** FAF-243

---

## Objectives

1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/tokenizer.
3. Implement a sample lexer and show how it works.

---

## Theory

Lexical analysis is the first stage of a compiler or interpreter. Its job is to read a raw string of characters and split it into meaningful chunks called **tokens**. Each token has a **type** (what kind of thing it is) and a **value** (the actual text).

For example, the string `SELECT age FROM users` becomes four tokens: `KEYWORD 'SELECT'`, `IDENTIFIER 'age'`, `KEYWORD 'FROM'`, `IDENTIFIER 'users'`. The next stage of a compiler (the parser) then works with this token list instead of raw characters.

A lexer is directly related to the finite automata studied in Lab 2. Each rule for recognising a token type corresponds to a state in a DFA: when the lexer sees a digit it stays in the "reading number" state until a non-digit appears, exactly as a DFA transitions between states on each input symbol.

---

## Implementation

### Overview

The lexer targets a simple subset of SQL. It was chosen because SQL has clearly distinct token categories — keywords, identifiers, string literals, numeric literals, operators — which makes it a good demonstration of lexical analysis without requiring a complex grammar.

### Token types

| Type | Description | Example |
|---|---|---|
| `KEYWORD` | Reserved SQL words | `SELECT`, `FROM`, `WHERE` |
| `IDENTIFIER` | Table and column names | `users`, `age`, `name` |
| `INTEGER` | Whole numbers | `18`, `30` |
| `FLOAT` | Decimal numbers | `3.14`, `99.9` |
| `STRING` | Text in single quotes | `'Alice'` |
| `OPERATOR` | Comparison and arithmetic | `=`, `>=`, `<=`, `<>`, `!=` |
| `LPAREN` / `RPAREN` | Parentheses | `(` `)` |
| `COMMA` | Argument separator | `,` |
| `SEMICOLON` | Statement terminator | `;` |
| `COMMENT` | Single-line comment | `-- note` |
| `UNKNOWN` | Unrecognised character | `@`, `#` |

### Token class

```python
class Token:
    def __init__(self, type, value):
        self.type  = type
        self.value = value
```

### Keyword set

Identifiers and keywords look the same to the character scanner — both are sequences of letters. After reading a full word, the lexer checks if it belongs to the keywords set. If yes it emits `KEYWORD`, otherwise `IDENTIFIER`.

```python
KEYWORDS = {"SELECT", "FROM", "WHERE", "INSERT", "INTO",
            "VALUES", "UPDATE", "SET", "DELETE", "AND", "OR", "NOT"}
```

### Lexer class

The `Lexer` class walks through the input one character at a time. The main `tokenize()` method dispatches to the right branch based on the current character:

Whitespace (`space`, `tab`, `newline`) is skipped without producing a token. A single quote starts a string — characters are consumed until the matching closing quote. A digit starts a number — digits are consumed and if a `.` is encountered the token becomes a `FLOAT`. A letter starts a word — letters and digits are consumed, then the result is looked up in `KEYWORDS`. Single characters like `=`, `(`, `,`, `;` are mapped directly to their token types. Anything else produces `UNKNOWN`.

### Main program

`main.py` runs the lexer on four SQL statements covering the main DML operations and prints the resulting tokens for each.

---

## Results

### SELECT

Input:
```sql
SELECT name, age FROM users WHERE age > 18;
```

Output:
```
Token(KEYWORD      'SELECT')
Token(IDENTIFIER   'name')
Token(COMMA        ',')
Token(IDENTIFIER   'age')
Token(KEYWORD      'FROM')
Token(IDENTIFIER   'users')
Token(KEYWORD      'WHERE')
Token(IDENTIFIER   'age')
Token(OPERATOR     '>')
Token(INTEGER      '18')
Token(SEMICOLON    ';')
```

### INSERT

Input:
```sql
INSERT INTO users (name, age) VALUES ('Alice', 30);
```

Output:
```
Token(KEYWORD      'INSERT')
Token(KEYWORD      'INTO')
Token(IDENTIFIER   'users')
Token(LPAREN       '(')
Token(IDENTIFIER   'name')
Token(COMMA        ',')
Token(IDENTIFIER   'age')
Token(RPAREN       ')')
Token(KEYWORD      'VALUES')
Token(LPAREN       '(')
Token(STRING       'Alice')
Token(COMMA        ',')
Token(INTEGER      '30')
Token(RPAREN       ')')
Token(SEMICOLON    ';')
```

### UPDATE

Input:
```sql
UPDATE users SET age = 31 WHERE name = 'Alice';
```

Output:
```
Token(KEYWORD      'UPDATE')
Token(IDENTIFIER   'users')
Token(KEYWORD      'SET')
Token(IDENTIFIER   'age')
Token(OPERATOR     '=')
Token(INTEGER      '31')
Token(KEYWORD      'WHERE')
Token(IDENTIFIER   'name')
Token(OPERATOR     '=')
Token(STRING       'Alice')
Token(SEMICOLON    ';')
```

### DELETE

Input:
```sql
DELETE FROM users WHERE age < 18;
```

Output:
```
Token(KEYWORD      'DELETE')
Token(KEYWORD      'FROM')
Token(IDENTIFIER   'users')
Token(KEYWORD      'WHERE')
Token(IDENTIFIER   'age')
Token(OPERATOR     '<')
Token(INTEGER      '18')
Token(SEMICOLON    ';')
```

---

## How to Run

**Requirements:** Python 3.8+, no external libraries.

```bash
python3 main.py
```

---

## Project Structure

```
laboratory-work-3/
├── lexer.py      # Token class, Lexer class
├── main.py       # Example queries and output
└── README.MD     # This file
```

---

## Conclusions

1. Implemented a working lexer for a SQL subset covering SELECT, INSERT, UPDATE, DELETE.
2. The lexer correctly distinguishes keywords from identifiers using a set lookup.
3. Integer and float literals are both supported.
4. String literals with single-quote delimiters are handled correctly.
5. Unrecognised characters produce UNKNOWN tokens instead of crashing.
6. The implementation demonstrates the direct link between lexer logic and the DFA theory from Lab 2 — each branch in the tokenizer corresponds to a DFA state.

---

## References

Cretu Dumitru, Vasile Drumea, Irina Cojuhari — course materials FLFA.
LLVM Tutorial — My First Language Frontend: https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html
Wikipedia — Lexical analysis: https://en.wikipedia.org/wiki/Lexical_analysis

from lexer import Lexer

queries = [
    "SELECT name, age FROM users WHERE age > 18;",
    "SELECT name FROM users WHERE age >= 18 AND age <> 99;",
    "INSERT INTO users (name, age) VALUES ('Alice', 30);",
    "UPDATE users SET age = 31 WHERE name = 'Alice';",
    "DELETE FROM users WHERE age < 18;",
    "-- this is a comment\nSELECT * FROM users WHERE age != 0;",
]

for q in queries:
    print(f"\nInput: {q}")
    print("-" * 50)
    tokens = Lexer(q).tokenize()
    for tok in tokens:
        print(f"  {tok}")

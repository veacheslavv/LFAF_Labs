

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from lexer import Lexer, LexerError
from parser import Parser, ParseError
from ast_printer import ASTPrinter


# ─── helpers ────────────────────────────────────────────────────────────────

def run(sql: str, label: str = "") -> None:
    sep = "─" * 60
    print(f"\n{sep}")
    if label:
        print(f"  {label}")
    print(f"  SQL: {sql.strip()}")
    print(sep)

    try:
        tokens = Lexer(sql).tokenize()
        ast    = Parser(tokens).parse()
        tree   = ASTPrinter().print(ast)
        print(tree)
    except (LexerError, ParseError) as exc:
        print(f"ERROR: {exc}")


# ─── demo queries ────────────────────────────────────────────────────────────

QUERIES = [
    (
        "Simple SELECT *",
        "SELECT * FROM users;"
    ),
    (
        "SELECT with WHERE and ORDER BY",
        """
        SELECT id, name, email
        FROM users
        WHERE age > 18 AND active = TRUE
        ORDER BY name ASC
        LIMIT 10;
        """
    ),
    (
        "SELECT with JOIN",
        """
        SELECT u.name, o.total
        FROM users u
        INNER JOIN orders o ON u.id = o.user_id
        WHERE o.total > 100;
        """
    ),
    (
        "SELECT with aggregate function and GROUP BY / HAVING",
        """
        SELECT department, COUNT(DISTINCT id) AS emp_count, AVG(salary)
        FROM employees
        GROUP BY department
        HAVING COUNT(id) > 5
        ORDER BY emp_count DESC;
        """
    ),
    (
        "SELECT with BETWEEN, LIKE, IN",
        """
        SELECT name FROM products
        WHERE price BETWEEN 10.0 AND 99.99
          AND name LIKE '%phone%'
          AND category_id IN (1, 2, 3);
        """
    ),
    (
        "SELECT with IS NULL / IS NOT NULL",
        """
        SELECT * FROM employees
        WHERE manager_id IS NULL;
        """
    ),
    (
        "INSERT statement",
        """
        INSERT INTO users (name, email, age)
        VALUES ('Alice', 'alice@example.com', 30);
        """
    ),
    (
        "UPDATE statement",
        """
        UPDATE products
        SET price = 49.99, stock = stock - 1
        WHERE id = 42;
        """
    ),
    (
        "DELETE statement",
        """
        DELETE FROM sessions
        WHERE expires_at < '2024-01-01';
        """
    ),
    (
        "CREATE TABLE",
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INT PRIMARY KEY NOT NULL,
            user_id INT NOT NULL,
            total FLOAT,
            status VARCHAR(50) DEFAULT 'pending',
            created_at DATE
        );
        """
    ),
    (
        "DROP TABLE",
        "DROP TABLE IF EXISTS temp_cache;"
    ),
    (
        "LEFT JOIN + subexpression",
        """
        SELECT p.title, COUNT(r.id) AS reviews
        FROM posts p
        LEFT JOIN reviews r ON r.post_id = p.id
        WHERE p.published = TRUE
        GROUP BY p.title
        ORDER BY reviews DESC
        LIMIT 5;
        """
    ),
]


def main():
    for label, sql in QUERIES:
        run(sql, label)

    print(f"\n{'─' * 60}")
    print(f"  Processed {len(QUERIES)} queries successfully.")
    print(f"{'─' * 60}")


if __name__ == "__main__":
    main()

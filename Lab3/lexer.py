# token types
INTEGER    = "INTEGER"
FLOAT      = "FLOAT"
STRING     = "STRING"
KEYWORD    = "KEYWORD"
IDENTIFIER = "IDENTIFIER"
OPERATOR   = "OPERATOR"
LPAREN     = "LPAREN"
RPAREN     = "RPAREN"
COMMA      = "COMMA"
SEMICOLON  = "SEMICOLON"
COMMENT    = "COMMENT"
UNKNOWN    = "UNKNOWN"

KEYWORDS = {"SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES",
            "UPDATE", "SET", "DELETE", "AND", "OR", "NOT"}

class Token:
    def __init__(self, type, value):
        self.type  = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type:<12} {self.value!r})"


class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos    = 0

    def current(self):
        return self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self):
        idx = self.pos + 1
        return self.source[idx] if idx < len(self.source) else None

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        return ch

    def tokenize(self):
        tokens = []

        while self.pos < len(self.source):
            ch = self.current()

            # skip whitespace
            if ch in (" ", "\t", "\n", "\r"):
                self.advance()
                continue

            # single-line comment  --
            if ch == "-" and self.peek() == "-":
                buf = ""
                while self.current() and self.current() != "\n":
                    buf += self.advance()
                tokens.append(Token(COMMENT, buf))
                continue

            # string literal  '...'
            if ch == "'":
                self.advance()
                buf = ""
                while self.current() and self.current() != "'":
                    buf += self.advance()
                self.advance()  # closing quote
                tokens.append(Token(STRING, buf))
                continue

            # number
            if ch.isdigit():
                buf      = ""
                is_float = False
                while self.current() and (self.current().isdigit() or self.current() == "."):
                    if self.current() == ".":
                        is_float = True
                    buf += self.advance()
                tokens.append(Token(FLOAT if is_float else INTEGER, buf))
                continue

            # identifier or keyword
            if ch.isalpha() or ch == "_":
                buf = ""
                while self.current() and (self.current().isalnum() or self.current() == "_"):
                    buf += self.advance()
                ttype = KEYWORD if buf.upper() in KEYWORDS else IDENTIFIER
                tokens.append(Token(ttype, buf))
                continue

            # two-character operators: >=  <=  <>  !=
            two = ch + (self.peek() or "")
            if two in (">=", "<=", "<>", "!="):
                self.advance(); self.advance()
                tokens.append(Token(OPERATOR, two))
                continue

            # single-character operators
            if ch in ("=", "<", ">", "+", "-", "*", "/"):
                tokens.append(Token(OPERATOR, self.advance()))
                continue

            # delimiters
            if ch == "(":
                self.advance(); tokens.append(Token(LPAREN,    "(")); continue
            if ch == ")":
                self.advance(); tokens.append(Token(RPAREN,    ")")); continue
            if ch == ",":
                self.advance(); tokens.append(Token(COMMA,     ",")); continue
            if ch == ";":
                self.advance(); tokens.append(Token(SEMICOLON, ";")); continue

            # unknown
            tokens.append(Token(UNKNOWN, self.advance()))

        return tokens

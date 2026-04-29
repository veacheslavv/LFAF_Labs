"""
Lab 4 - Lexer (extended from Lab 3)
SQL Lexer with TokenType enum and regex-based token recognition.
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # Keywords
    SELECT   = auto()
    FROM     = auto()
    WHERE    = auto()
    INSERT   = auto()
    INTO     = auto()
    VALUES   = auto()
    UPDATE   = auto()
    SET      = auto()
    DELETE   = auto()
    CREATE   = auto()
    TABLE    = auto()
    DROP     = auto()
    AND      = auto()
    OR       = auto()
    NOT      = auto()
    NULL     = auto()
    IS       = auto()
    IN       = auto()
    LIKE     = auto()
    BETWEEN  = auto()
    ORDER    = auto()
    BY       = auto()
    ASC      = auto()
    DESC     = auto()
    LIMIT    = auto()
    JOIN     = auto()
    ON       = auto()
    AS       = auto()
    DISTINCT = auto()
    GROUP    = auto()
    HAVING   = auto()
    LEFT     = auto()
    RIGHT    = auto()
    INNER    = auto()
    DEFAULT  = auto()
    IF       = auto()
    EXISTS   = auto()

    # Literals
    INTEGER_LITERAL = auto()
    FLOAT_LITERAL   = auto()
    STRING_LITERAL  = auto()
    BOOLEAN_LITERAL = auto()

    # Identifiers
    IDENTIFIER = auto()

    # Operators (all symbolic)
    EQ  = auto()   # =
    NEQ = auto()   # != / <>
    LT  = auto()   # <
    GT  = auto()   # >
    LTE = auto()   # <=
    GTE = auto()   # >=
    ADD = auto()   # +
    SUB = auto()   # -
    MUL = auto()   # *
    DIV = auto()   # /
    MOD = auto()   # %

    # Punctuation
    COMMA     = auto()
    SEMICOLON = auto()
    LPAREN    = auto()
    RPAREN    = auto()
    DOT       = auto()

    # Special
    WHITESPACE = auto()
    COMMENT    = auto()
    EOF        = auto()
    UNKNOWN    = auto()


# Map keyword strings → TokenType
KEYWORDS: dict[str, TokenType] = {
    kw.name: kw for kw in [
        TokenType.SELECT, TokenType.FROM, TokenType.WHERE,
        TokenType.INSERT, TokenType.INTO, TokenType.VALUES,
        TokenType.UPDATE, TokenType.SET, TokenType.DELETE,
        TokenType.CREATE, TokenType.TABLE, TokenType.DROP,
        TokenType.AND, TokenType.OR, TokenType.NOT,
        TokenType.NULL, TokenType.IS, TokenType.IN,
        TokenType.LIKE, TokenType.BETWEEN,
        TokenType.ORDER, TokenType.BY, TokenType.ASC, TokenType.DESC,
        TokenType.LIMIT, TokenType.JOIN, TokenType.ON, TokenType.AS,
        TokenType.DISTINCT, TokenType.GROUP, TokenType.HAVING,
        TokenType.LEFT, TokenType.RIGHT, TokenType.INNER,
        TokenType.DEFAULT, TokenType.IF, TokenType.EXISTS,
    ]
}

# Word operator → symbol (used by AST printer)
OP_SYMBOL: dict[str, str] = {
    "AND": "&&",
    "OR":  "||",
    "NOT": "!",
    "=":   "==",
    "<>":  "!=",
    "!=":  "!=",
}

# Regex patterns ordered by priority
TOKEN_PATTERNS: list[tuple[TokenType, re.Pattern]] = [
    (TokenType.COMMENT,         re.compile(r'--[^\n]*|/\*.*?\*/', re.DOTALL)),
    (TokenType.WHITESPACE,      re.compile(r'\s+')),
    (TokenType.FLOAT_LITERAL,   re.compile(r'\d+\.\d+')),
    (TokenType.INTEGER_LITERAL, re.compile(r'\d+')),
    (TokenType.STRING_LITERAL,  re.compile(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"")),
    (TokenType.NEQ,             re.compile(r'<>|!=')),
    (TokenType.LTE,             re.compile(r'<=')),
    (TokenType.GTE,             re.compile(r'>=')),
    (TokenType.EQ,              re.compile(r'=')),
    (TokenType.LT,              re.compile(r'<')),
    (TokenType.GT,              re.compile(r'>')),
    (TokenType.ADD,             re.compile(r'\+')),
    (TokenType.SUB,             re.compile(r'-')),
    (TokenType.MUL,             re.compile(r'\*')),
    (TokenType.DIV,             re.compile(r'/')),
    (TokenType.MOD,             re.compile(r'%')),
    (TokenType.COMMA,           re.compile(r',')),
    (TokenType.SEMICOLON,       re.compile(r';')),
    (TokenType.LPAREN,          re.compile(r'\(')),
    (TokenType.RPAREN,          re.compile(r'\)')),
    (TokenType.DOT,             re.compile(r'\.')),
    (TokenType.IDENTIFIER,      re.compile(r'[A-Za-z_][A-Za-z0-9_]*')),
]


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError at line {line}, col {column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    def tokenize(self, skip_whitespace: bool = True, skip_comments: bool = True) -> List[Token]:
        tokens: List[Token] = []
        while self.pos < len(self.source):
            token = self._next_token()
            if token is None:
                raise LexerError(
                    f"Unexpected character {self.source[self.pos]!r}",
                    self.line, self.column
                )
            if skip_whitespace and token.type == TokenType.WHITESPACE:
                continue
            if skip_comments and token.type == TokenType.COMMENT:
                continue
            tokens.append(token)
        tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return tokens

    def _next_token(self) -> Optional[Token]:
        remaining = self.source[self.pos:]
        for token_type, pattern in TOKEN_PATTERNS:
            m = pattern.match(remaining)
            if m:
                value = m.group(0)
                tok_line, tok_col = self.line, self.column

                if token_type == TokenType.IDENTIFIER:
                    upper = value.upper()
                    if upper in KEYWORDS:
                        token_type = KEYWORDS[upper]
                    elif upper in ('TRUE', 'FALSE'):
                        token_type = TokenType.BOOLEAN_LITERAL

                for ch in value:
                    if ch == '\n':
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += 1
                self.pos += len(value)
                return Token(token_type, value, tok_line, tok_col)

        ch = self.source[self.pos]
        tok = Token(TokenType.UNKNOWN, ch, self.line, self.column)
        self.pos += 1
        self.column += 1
        return tok

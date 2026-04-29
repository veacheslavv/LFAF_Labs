"""
Lab 4 - SQL Parser
Recursive-descent parser that converts a token stream into an AST.
"""

from typing import List, Optional
from lexer import Token, TokenType
from ast_nodes import *


class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(
            f"ParseError at line {token.line}, col {token.column} "
            f"[{token.type.name} {token.value!r}]: {message}"
        )
        self.token = token


class Parser:
    """
    Recursive-descent parser for a subset of SQL.

    Grammar (simplified):
        program     → statement* EOF
        statement   → select_stmt | insert_stmt | update_stmt
                    | delete_stmt | create_stmt | drop_stmt
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    # ── helpers ─────────────────────────────────────────────────────────

    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def peek(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        return self.tokens[min(idx, len(self.tokens) - 1)]

    def check(self, *types: TokenType) -> bool:
        return self.current.type in types

    def advance(self) -> Token:
        tok = self.current
        if tok.type != TokenType.EOF:
            self.pos += 1
        return tok

    def expect(self, *types: TokenType) -> Token:
        if not self.check(*types):
            expected = " or ".join(t.name for t in types)
            raise ParseError(
                f"Expected {expected}, got {self.current.type.name}",
                self.current,
            )
        return self.advance()

    def match(self, *types: TokenType) -> Optional[Token]:
        if self.check(*types):
            return self.advance()
        return None

    def at_end(self) -> bool:
        return self.current.type == TokenType.EOF

    # ── entry ────────────────────────────────────────────────────────────

    def parse(self) -> Program:
        statements: List[ASTNode] = []
        while not self.at_end():
            statements.append(self._statement())
            self.match(TokenType.SEMICOLON)
        return Program(statements=statements)

    # ── statements ───────────────────────────────────────────────────────

    def _statement(self) -> ASTNode:
        tok = self.current
        if self.check(TokenType.SELECT):  return self._select_stmt()
        if self.check(TokenType.INSERT):  return self._insert_stmt()
        if self.check(TokenType.UPDATE):  return self._update_stmt()
        if self.check(TokenType.DELETE):  return self._delete_stmt()
        if self.check(TokenType.CREATE):  return self._create_stmt()
        if self.check(TokenType.DROP):    return self._drop_stmt()
        raise ParseError(f"Unexpected token at start of statement: {tok.type.name}", tok)

    # ── SELECT ───────────────────────────────────────────────────────────

    def _select_stmt(self) -> SelectStatement:
        self.expect(TokenType.SELECT)
        distinct = bool(self.match(TokenType.DISTINCT))
        items = self._select_list()
        select_list = SelectList(items=items, distinct=distinct)

        from_table: Optional[TableReference] = None
        joins: List[JoinClause] = []
        if self.match(TokenType.FROM):
            from_table = self._table_ref()
            joins = self._join_clauses()

        where    = self._where_clause()
        group_by = self._group_by_clause()
        having   = self._having_clause()
        order_by = self._order_by_clause()
        limit    = self._limit_clause()

        return SelectStatement(
            select_list=select_list, from_table=from_table, joins=joins,
            where=where, group_by=group_by, having=having,
            order_by=order_by, limit=limit,
        )

    def _select_list(self) -> List[ASTNode]:
        items = [self._select_item()]
        while self.match(TokenType.COMMA):
            items.append(self._select_item())
        return items

    def _select_item(self) -> ASTNode:
        if self.check(TokenType.MUL):
            self.advance()
            return Wildcard()
        expr = self._expression()
        if self.match(TokenType.AS):
            alias = self.expect(TokenType.IDENTIFIER)
            return Alias(expression=expr, alias=alias.value)
        if self.check(TokenType.IDENTIFIER):
            return Alias(expression=expr, alias=self.advance().value)
        return expr

    # ── INSERT ───────────────────────────────────────────────────────────

    def _insert_stmt(self) -> InsertStatement:
        self.expect(TokenType.INSERT)
        self.expect(TokenType.INTO)
        table = self._table_ref()

        columns: List[Identifier] = []
        if self.match(TokenType.LPAREN):
            columns.append(Identifier(name=self.expect(TokenType.IDENTIFIER).value))
            while self.match(TokenType.COMMA):
                columns.append(Identifier(name=self.expect(TokenType.IDENTIFIER).value))
            self.expect(TokenType.RPAREN)

        self.expect(TokenType.VALUES)
        self.expect(TokenType.LPAREN)
        values = [self._expression()]
        while self.match(TokenType.COMMA):
            values.append(self._expression())
        self.expect(TokenType.RPAREN)

        return InsertStatement(table=table, columns=columns, values=values)

    # ── UPDATE ───────────────────────────────────────────────────────────

    def _update_stmt(self) -> UpdateStatement:
        self.expect(TokenType.UPDATE)
        table = self._table_ref()
        self.expect(TokenType.SET)
        assignments = [self._assignment()]
        while self.match(TokenType.COMMA):
            assignments.append(self._assignment())
        return UpdateStatement(table=table, assignments=assignments, where=self._where_clause())

    def _assignment(self) -> AssignmentClause:
        col = Identifier(name=self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.EQ)
        return AssignmentClause(column=col, value=self._expression())

    # ── DELETE ───────────────────────────────────────────────────────────

    def _delete_stmt(self) -> DeleteStatement:
        self.expect(TokenType.DELETE)
        self.expect(TokenType.FROM)
        return DeleteStatement(table=self._table_ref(), where=self._where_clause())

    # ── CREATE TABLE ─────────────────────────────────────────────────────

    def _create_stmt(self) -> CreateTableStatement:
        self.expect(TokenType.CREATE)
        self.expect(TokenType.TABLE)

        if_not_exists = False
        if self.match(TokenType.IF):
            self.expect(TokenType.NOT)
            self.expect(TokenType.EXISTS)
            if_not_exists = True

        table_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        columns = [self._column_def()]
        while self.match(TokenType.COMMA):
            columns.append(self._column_def())
        self.expect(TokenType.RPAREN)

        return CreateTableStatement(
            table_name=table_name, if_not_exists=if_not_exists, columns=columns
        )

    def _column_def(self) -> ColumnDefinition:
        name = self.expect(TokenType.IDENTIFIER).value
        # Data type is any identifier (INT, VARCHAR, TEXT, etc.)
        type_tok = self.expect(TokenType.IDENTIFIER)
        data_type = type_tok.value.upper()
        if self.match(TokenType.LPAREN):
            size = self.expect(TokenType.INTEGER_LITERAL).value
            data_type += f"({size})"
            self.expect(TokenType.RPAREN)

        nullable, primary_key, unique, default = True, False, False, None

        # Inline constraints: NOT NULL, PRIMARY KEY, UNIQUE, DEFAULT expr
        while self.check(TokenType.NOT, TokenType.IDENTIFIER, TokenType.DEFAULT):
            if self.check(TokenType.NOT):
                self.advance()
                self.expect(TokenType.NULL)
                nullable = False
            elif self.check(TokenType.IDENTIFIER) and self.current.value.upper() == 'PRIMARY':
                self.advance()
                if self.check(TokenType.IDENTIFIER) and self.current.value.upper() == 'KEY':
                    self.advance()
                primary_key = True
            elif self.check(TokenType.IDENTIFIER) and self.current.value.upper() == 'UNIQUE':
                self.advance()
                unique = True
            elif self.match(TokenType.DEFAULT):
                default = self._expression()
            else:
                break

        return ColumnDefinition(
            name=name, data_type=data_type,
            nullable=nullable, primary_key=primary_key,
            unique=unique, default=default,
        )

    # ── DROP TABLE ───────────────────────────────────────────────────────

    def _drop_stmt(self) -> DropTableStatement:
        self.expect(TokenType.DROP)
        self.expect(TokenType.TABLE)
        if_exists = False
        if self.match(TokenType.IF):
            self.expect(TokenType.EXISTS)
            if_exists = True
        return DropTableStatement(
            table_name=self.expect(TokenType.IDENTIFIER).value,
            if_exists=if_exists,
        )

    # ── Shared clauses ───────────────────────────────────────────────────

    _CLAUSE_KW = {
        TokenType.WHERE, TokenType.JOIN, TokenType.INNER,
        TokenType.LEFT, TokenType.RIGHT,
        TokenType.ORDER, TokenType.GROUP, TokenType.HAVING,
        TokenType.LIMIT, TokenType.SEMICOLON, TokenType.EOF,
    }

    def _table_ref(self) -> TableReference:
        name = self.expect(TokenType.IDENTIFIER).value
        alias: Optional[str] = None
        if self.match(TokenType.AS):
            alias = self.expect(TokenType.IDENTIFIER).value
        elif self.check(TokenType.IDENTIFIER) and self.current.type not in self._CLAUSE_KW:
            alias = self.advance().value
        return TableReference(name=name, alias=alias)

    def _join_clauses(self) -> List[JoinClause]:
        joins = []
        while self.check(TokenType.JOIN, TokenType.INNER, TokenType.LEFT, TokenType.RIGHT):
            join_type = "INNER"
            if self.match(TokenType.LEFT):
                join_type = "LEFT"
            elif self.match(TokenType.RIGHT):
                join_type = "RIGHT"
            elif self.match(TokenType.INNER):
                join_type = "INNER"
            self.expect(TokenType.JOIN)
            table = self._table_ref()
            condition = None
            if self.match(TokenType.ON):
                condition = self._expression()
            joins.append(JoinClause(join_type=join_type, table=table, condition=condition))
        return joins

    def _where_clause(self) -> Optional[WhereClause]:
        if self.match(TokenType.WHERE):
            return WhereClause(condition=self._expression())
        return None

    def _group_by_clause(self) -> Optional[GroupByClause]:
        if self.match(TokenType.GROUP):
            self.expect(TokenType.BY)
            cols = [self._expression()]
            while self.match(TokenType.COMMA):
                cols.append(self._expression())
            return GroupByClause(columns=cols)
        return None

    def _having_clause(self) -> Optional[HavingClause]:
        if self.match(TokenType.HAVING):
            return HavingClause(condition=self._expression())
        return None

    def _order_by_clause(self) -> Optional[OrderByClause]:
        if self.match(TokenType.ORDER):
            self.expect(TokenType.BY)
            items = [self._order_item()]
            while self.match(TokenType.COMMA):
                items.append(self._order_item())
            return OrderByClause(items=items)
        return None

    def _order_item(self) -> OrderByItem:
        expr = self._expression()
        direction = "DESC" if self.match(TokenType.DESC) else "ASC"
        self.match(TokenType.ASC)
        return OrderByItem(expression=expr, direction=direction)

    def _limit_clause(self) -> Optional[LimitClause]:
        if self.match(TokenType.LIMIT):
            return LimitClause(count=self._expression())
        return None

    # ── Expressions (precedence climbing) ────────────────────────────────

    def _expression(self) -> ASTNode:
        return self._or_expr()

    def _or_expr(self) -> ASTNode:
        left = self._and_expr()
        while self.match(TokenType.OR):
            left = BinaryExpression(left=left, operator="||", right=self._and_expr())
        return left

    def _and_expr(self) -> ASTNode:
        left = self._not_expr()
        while self.match(TokenType.AND):
            left = BinaryExpression(left=left, operator="&&", right=self._not_expr())
        return left

    def _not_expr(self) -> ASTNode:
        if self.match(TokenType.NOT):
            return UnaryExpression(operator="!", operand=self._not_expr())
        return self._comparison()

    def _comparison(self) -> ASTNode:
        left = self._additive()

        # IS [NOT] NULL
        if self.match(TokenType.IS):
            negated = bool(self.match(TokenType.NOT))
            self.expect(TokenType.NULL)
            return IsNullExpression(expression=left, negated=negated)

        negated = bool(self.match(TokenType.NOT))

        if self.match(TokenType.BETWEEN):
            low = self._additive()
            self.expect(TokenType.AND)
            high = self._additive()
            return BetweenExpression(expression=left, low=low, high=high, negated=negated)

        if self.match(TokenType.LIKE):
            return LikeExpression(expression=left, pattern=self._additive(), negated=negated)

        if self.match(TokenType.IN):
            self.expect(TokenType.LPAREN)
            values = [self._expression()]
            while self.match(TokenType.COMMA):
                values.append(self._expression())
            self.expect(TokenType.RPAREN)
            return InExpression(expression=left, values=values, negated=negated)

        if negated:
            raise ParseError("! used without BETWEEN, LIKE, or IN", self.current)

        op_map = {
            TokenType.EQ:  "==",
            TokenType.NEQ: "!=",
            TokenType.LT:  "<",
            TokenType.GT:  ">",
            TokenType.LTE: "<=",
            TokenType.GTE: ">=",
        }
        if self.current.type in op_map:
            sym = op_map[self.advance().type]
            return BinaryExpression(left=left, operator=sym, right=self._additive())

        return left

    def _additive(self) -> ASTNode:
        left = self._multiplicative()
        while self.check(TokenType.ADD, TokenType.SUB):
            op = self.advance().value   # '+' or '-'
            left = BinaryExpression(left=left, operator=op, right=self._multiplicative())
        return left

    def _multiplicative(self) -> ASTNode:
        left = self._unary()
        while self.check(TokenType.MUL, TokenType.DIV, TokenType.MOD):
            op = self.advance().value
            left = BinaryExpression(left=left, operator=op, right=self._unary())
        return left

    def _unary(self) -> ASTNode:
        if self.check(TokenType.SUB, TokenType.ADD):
            return UnaryExpression(operator=self.advance().value, operand=self._unary())
        return self._primary()

    def _primary(self) -> ASTNode:
        tok = self.current

        if self.match(TokenType.NULL):            return NullLiteral()
        if self.match(TokenType.BOOLEAN_LITERAL): return BooleanLiteral(value=tok.value.upper() == 'TRUE')
        if self.match(TokenType.INTEGER_LITERAL): return IntegerLiteral(value=int(tok.value))
        if self.match(TokenType.FLOAT_LITERAL):   return FloatLiteral(value=float(tok.value))
        if self.match(TokenType.STRING_LITERAL):  return StringLiteral(value=tok.value[1:-1])
        if self.match(TokenType.MUL):             return Wildcard()

        if self.match(TokenType.LPAREN):
            expr = self._expression()
            self.expect(TokenType.RPAREN)
            return expr

        if self.check(TokenType.IDENTIFIER):
            name = self.advance().value
            # Function call
            if self.match(TokenType.LPAREN):
                distinct = bool(self.match(TokenType.DISTINCT))
                args: List[ASTNode] = []
                if not self.check(TokenType.RPAREN):
                    args.append(self._expression())
                    while self.match(TokenType.COMMA):
                        args.append(self._expression())
                self.expect(TokenType.RPAREN)
                return FunctionCall(name=name.upper(), arguments=args, distinct=distinct)
            # Qualified identifier table.column or table.*
            parts = [name]
            while self.match(TokenType.DOT):
                if self.match(TokenType.MUL):
                    return Wildcard(table=name)
                parts.append(self.expect(TokenType.IDENTIFIER).value)
            return Identifier(name=parts[0]) if len(parts) == 1 else QualifiedIdentifier(parts=parts)

        raise ParseError(f"Unexpected token in expression: {tok.type.name}", tok)
      

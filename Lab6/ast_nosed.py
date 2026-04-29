"""
Lab 4 - AST Node Definitions
Hierarchical data structures representing SQL constructs.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union


# ─────────────────────────────────────────────────
#  Base
# ─────────────────────────────────────────────────

class ASTNode:
    """Base class for all AST nodes."""

    def accept(self, visitor: "ASTVisitor"):
        method = f"visit_{type(self).__name__}"
        return getattr(visitor, method, visitor.generic_visit)(self)

    def __repr__(self):
        fields = ", ".join(
            f"{k}={v!r}" for k, v in self.__dict__.items()
        )
        return f"{type(self).__name__}({fields})"


# ─────────────────────────────────────────────────
#  Literals & Identifiers
# ─────────────────────────────────────────────────

@dataclass
class IntegerLiteral(ASTNode):
    value: int


@dataclass
class FloatLiteral(ASTNode):
    value: float


@dataclass
class StringLiteral(ASTNode):
    value: str


@dataclass
class BooleanLiteral(ASTNode):
    value: bool


@dataclass
class NullLiteral(ASTNode):
    pass


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class QualifiedIdentifier(ASTNode):
    """table.column or schema.table.column"""
    parts: List[str]

    @property
    def full_name(self) -> str:
        return ".".join(self.parts)


@dataclass
class Wildcard(ASTNode):
    """Represents '*' or 'table.*'"""
    table: Optional[str] = None


@dataclass
class Alias(ASTNode):
    """expression AS alias"""
    expression: ASTNode
    alias: str


# ─────────────────────────────────────────────────
#  Expressions
# ─────────────────────────────────────────────────

@dataclass
class BinaryExpression(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryExpression(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class BetweenExpression(ASTNode):
    expression: ASTNode
    low: ASTNode
    high: ASTNode
    negated: bool = False


@dataclass
class InExpression(ASTNode):
    expression: ASTNode
    values: List[ASTNode]
    negated: bool = False


@dataclass
class LikeExpression(ASTNode):
    expression: ASTNode
    pattern: ASTNode
    negated: bool = False


@dataclass
class IsNullExpression(ASTNode):
    expression: ASTNode
    negated: bool = False


@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: List[ASTNode]
    distinct: bool = False


# ─────────────────────────────────────────────────
#  Column & Table references
# ─────────────────────────────────────────────────

@dataclass
class ColumnDefinition(ASTNode):
    name: str
    data_type: str
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: Optional[ASTNode] = None


@dataclass
class TableReference(ASTNode):
    name: str
    alias: Optional[str] = None


@dataclass
class JoinClause(ASTNode):
    join_type: str          # INNER, LEFT, RIGHT, FULL, CROSS
    table: TableReference
    condition: Optional[ASTNode] = None


# ─────────────────────────────────────────────────
#  Clauses
# ─────────────────────────────────────────────────

@dataclass
class SelectList(ASTNode):
    items: List[ASTNode]
    distinct: bool = False


@dataclass
class WhereClause(ASTNode):
    condition: ASTNode


@dataclass
class OrderByItem(ASTNode):
    expression: ASTNode
    direction: str = "ASC"


@dataclass
class OrderByClause(ASTNode):
    items: List[OrderByItem]


@dataclass
class GroupByClause(ASTNode):
    columns: List[ASTNode]


@dataclass
class HavingClause(ASTNode):
    condition: ASTNode


@dataclass
class LimitClause(ASTNode):
    count: ASTNode


@dataclass
class AssignmentClause(ASTNode):
    """col = expr used in UPDATE SET"""
    column: Identifier
    value: ASTNode


# ─────────────────────────────────────────────────
#  Statements
# ─────────────────────────────────────────────────

@dataclass
class SelectStatement(ASTNode):
    select_list: SelectList
    from_table: Optional[TableReference]
    joins: List[JoinClause] = field(default_factory=list)
    where: Optional[WhereClause] = None
    group_by: Optional[GroupByClause] = None
    having: Optional[HavingClause] = None
    order_by: Optional[OrderByClause] = None
    limit: Optional[LimitClause] = None


@dataclass
class InsertStatement(ASTNode):
    table: TableReference
    columns: List[Identifier]
    values: List[ASTNode]


@dataclass
class UpdateStatement(ASTNode):
    table: TableReference
    assignments: List[AssignmentClause]
    where: Optional[WhereClause] = None


@dataclass
class DeleteStatement(ASTNode):
    table: TableReference
    where: Optional[WhereClause] = None


@dataclass
class CreateTableStatement(ASTNode):
    table_name: str
    if_not_exists: bool
    columns: List[ColumnDefinition]


@dataclass
class DropTableStatement(ASTNode):
    table_name: str
    if_exists: bool


@dataclass
class Program(ASTNode):
    """Root node - a list of SQL statements."""
    statements: List[ASTNode]


# ─────────────────────────────────────────────────
#  Visitor base
# ─────────────────────────────────────────────────

class ASTVisitor:
    """Base visitor. Override visit_* methods to process nodes."""

    def generic_visit(self, node: ASTNode):
        raise NotImplementedError(
            f"No visitor method for {type(node).__name__}"
        )

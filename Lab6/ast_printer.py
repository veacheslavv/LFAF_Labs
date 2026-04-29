"""
Lab 4 - AST Printer
Pretty-prints an AST in a readable tree format.
"""

from ast_nodes import *


class ASTPrinter(ASTVisitor):
    """Converts an AST back to a readable indented tree representation."""

    def __init__(self):
        self.indent = 0
        self._lines: list[str] = []

    def _line(self, text: str):
        self._lines.append("  " * self.indent + text)

    def _child(self, label: str, node: Optional[ASTNode]):
        if node is None:
            return
        self._line(f"{label}:")
        self.indent += 1
        node.accept(self)
        self.indent -= 1

    def _children(self, label: str, nodes: list):
        if not nodes:
            return
        self._line(f"{label}:")
        self.indent += 1
        for n in nodes:
            n.accept(self)
        self.indent -= 1

    def print(self, node: ASTNode) -> str:
        self._lines = []
        node.accept(self)
        return "\n".join(self._lines)

    # ── Visitors ────────────────────────────────────────────────────────

    def visit_Program(self, node: Program):
        self._line("Program")
        self.indent += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.indent -= 1

    def visit_SelectStatement(self, node: SelectStatement):
        self._line("SelectStatement")
        self.indent += 1
        node.select_list.accept(self)
        if node.from_table:
            self._child("FROM", node.from_table)
        self._children("JOINS", node.joins)
        self._child("WHERE", node.where)
        self._child("GROUP BY", node.group_by)
        self._child("HAVING", node.having)
        self._child("ORDER BY", node.order_by)
        self._child("LIMIT", node.limit)
        self.indent -= 1

    def visit_SelectList(self, node: SelectList):
        label = "SelectList (DISTINCT)" if node.distinct else "SelectList"
        self._line(label)
        self.indent += 1
        for item in node.items:
            item.accept(self)
        self.indent -= 1

    def visit_InsertStatement(self, node: InsertStatement):
        self._line("InsertStatement")
        self.indent += 1
        self._child("INTO", node.table)
        self._children("COLUMNS", node.columns)
        self._children("VALUES", node.values)
        self.indent -= 1

    def visit_UpdateStatement(self, node: UpdateStatement):
        self._line("UpdateStatement")
        self.indent += 1
        self._child("TABLE", node.table)
        self._children("SET", node.assignments)
        self._child("WHERE", node.where)
        self.indent -= 1

    def visit_DeleteStatement(self, node: DeleteStatement):
        self._line("DeleteStatement")
        self.indent += 1
        self._child("FROM", node.table)
        self._child("WHERE", node.where)
        self.indent -= 1

    def visit_CreateTableStatement(self, node: CreateTableStatement):
        suffix = " (IF NOT EXISTS)" if node.if_not_exists else ""
        self._line(f"CreateTableStatement: {node.table_name}{suffix}")
        self.indent += 1
        self._children("COLUMNS", node.columns)
        self.indent -= 1

    def visit_DropTableStatement(self, node: DropTableStatement):
        suffix = " (IF EXISTS)" if node.if_exists else ""
        self._line(f"DropTableStatement: {node.table_name}{suffix}")

    def visit_TableReference(self, node: TableReference):
        alias = f" AS {node.alias}" if node.alias else ""
        self._line(f"TableRef: {node.name}{alias}")

    def visit_JoinClause(self, node: JoinClause):
        self._line(f"Join ({node.join_type})")
        self.indent += 1
        node.table.accept(self)
        self._child("ON", node.condition)
        self.indent -= 1

    def visit_WhereClause(self, node: WhereClause):
        node.condition.accept(self)

    def visit_GroupByClause(self, node: GroupByClause):
        self._children("columns", node.columns)

    def visit_HavingClause(self, node: HavingClause):
        node.condition.accept(self)

    def visit_OrderByClause(self, node: OrderByClause):
        for item in node.items:
            item.accept(self)

    def visit_OrderByItem(self, node: OrderByItem):
        self._line(f"OrderByItem ({node.direction})")
        self.indent += 1
        node.expression.accept(self)
        self.indent -= 1

    def visit_LimitClause(self, node: LimitClause):
        node.count.accept(self)

    def visit_ColumnDefinition(self, node: ColumnDefinition):
        flags = []
        if node.primary_key: flags.append("PRIMARY KEY")
        if node.unique:       flags.append("UNIQUE")
        if not node.nullable: flags.append("NOT NULL")
        flag_str = ", ".join(flags)
        suffix = f" [{flag_str}]" if flags else ""
        self._line(f"ColumnDef: {node.name} {node.data_type}{suffix}")
        if node.default:
            self._child("DEFAULT", node.default)

    def visit_AssignmentClause(self, node: AssignmentClause):
        self._line(f"Assign: {node.column.name}")
        self.indent += 1
        node.value.accept(self)
        self.indent -= 1

    def visit_BinaryExpression(self, node: BinaryExpression):
        self._line(f"BinaryExpr ({node.operator})")
        self.indent += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent -= 1

    def visit_UnaryExpression(self, node: UnaryExpression):
        self._line(f"UnaryExpr ({node.operator})")
        self.indent += 1
        node.operand.accept(self)
        self.indent -= 1

    def visit_BetweenExpression(self, node: BetweenExpression):
        label = "NOT BETWEEN" if node.negated else "BETWEEN"
        self._line(label)
        self.indent += 1
        node.expression.accept(self)
        node.low.accept(self)
        node.high.accept(self)
        self.indent -= 1

    def visit_InExpression(self, node: InExpression):
        label = "NOT IN" if node.negated else "IN"
        self._line(label)
        self.indent += 1
        node.expression.accept(self)
        self._children("values", node.values)
        self.indent -= 1

    def visit_LikeExpression(self, node: LikeExpression):
        label = "NOT LIKE" if node.negated else "LIKE"
        self._line(label)
        self.indent += 1
        node.expression.accept(self)
        node.pattern.accept(self)
        self.indent -= 1

    def visit_IsNullExpression(self, node: IsNullExpression):
        label = "IS NOT NULL" if node.negated else "IS NULL"
        self._line(label)
        self.indent += 1
        node.expression.accept(self)
        self.indent -= 1

    def visit_FunctionCall(self, node: FunctionCall):
        distinct = " DISTINCT" if node.distinct else ""
        self._line(f"FunctionCall: {node.name}{distinct}()")
        self.indent += 1
        for arg in node.arguments:
            arg.accept(self)
        self.indent -= 1

    def visit_Identifier(self, node: Identifier):
        self._line(f"Identifier: {node.name}")

    def visit_QualifiedIdentifier(self, node: QualifiedIdentifier):
        self._line(f"QualifiedIdentifier: {node.full_name}")

    def visit_Wildcard(self, node: Wildcard):
        table = f"{node.table}." if node.table else ""
        self._line(f"Wildcard: {table}*")

    def visit_Alias(self, node: Alias):
        self._line(f"Alias: AS {node.alias}")
        self.indent += 1
        node.expression.accept(self)
        self.indent -= 1

    def visit_IntegerLiteral(self, node: IntegerLiteral):
        self._line(f"IntLiteral: {node.value}")

    def visit_FloatLiteral(self, node: FloatLiteral):
        self._line(f"FloatLiteral: {node.value}")

    def visit_StringLiteral(self, node: StringLiteral):
        self._line(f"StringLiteral: '{node.value}'")

    def visit_BooleanLiteral(self, node: BooleanLiteral):
        self._line(f"BoolLiteral: {node.value}")

    def visit_NullLiteral(self, node: NullLiteral):
        self._line("NullLiteral")

from src.ast import Ast, BinaryOp, Constant, FunCall, FunDecl, Identifier, MatDecl, UnaryOp, VarDecl, Visitor

class RenderVisitor(Visitor):
	"""This visitor that renders the AST using the minimum amount of parentheses possible."""

	def visit(self, node: Ast) -> None:
		node.accept(self)
		print()

	def _need_parentheses(self, parent: BinaryOp, child, assoc):
		if isinstance(child, (BinaryOp, UnaryOp)):
			return parent.get_precedence() > child.get_precedence() \
				or (parent.get_precedence() == child.get_precedence()
				and parent.get_associativity() == assoc)
		return False

	def _render_grouped(self, node, need_parenthesis):
		if need_parenthesis:
			print('(', end='')
		node.accept(self)
		if need_parenthesis:
			print(')', end='')

	def _render_funcall(self, name, args):
		print(name, end='')
		print('(', end='')
		for i, arg in enumerate(args):
			if i > 0:
				print(', ', end='')
			arg.accept(self)
		print(')', end='')

	def visit_constant(self, constant: Constant) -> None:
		print(constant, end='')

	def visit_identifier(self, id: Identifier) -> None:
		print(id, end='')

	def visit_vardecl(self, vardecl: VarDecl) -> None:
		vardecl.id.accept(self)
		print(' = ', end='')
		vardecl.value.accept(self)

	def visit_matdecl(self, matdecl: MatDecl) -> None:
		print('[', end='')
		for i, row in enumerate(matdecl.rows):
			if i > 0:
				print('; ', end='')
			print(row, end='')
		print(']', end='')

	def visit_fundecl(self, fundecl: FunDecl) -> None:
		self._render_funcall(fundecl.id, fundecl.args)
		print(' = ', end='')
		fundecl.body.accept(self)

	def visit_funcall(self, funcall: FunCall) -> None:
		self._render_funcall(funcall.id, funcall.args)

	def visit_binaryop(self, binop: BinaryOp) -> None:
		left_parentheses = self._need_parentheses(binop, binop.left, 'right')
		right_parentheses = self._need_parentheses(binop, binop.right, 'left')
		self._render_grouped(binop.left, left_parentheses)
		if binop.op != '*' or not (isinstance(binop.left, Constant) \
			and isinstance(binop.right, Identifier)):
			print(f' {binop.op} ', end='')
		self._render_grouped(binop.right, right_parentheses)

	def visit_unaryop(self, unop: UnaryOp) -> None:
		need_parentheses = isinstance(unop.right, (BinaryOp, UnaryOp)) \
			and unop.get_precedence() > unop.right.get_precedence()
		if unop.op == '-':
			print(unop.op, end='')
		self._render_grouped(unop.right, need_parentheses)

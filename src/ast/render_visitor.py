from src.ast import Ast, BinaryOp, Constant, FunCall, FunDecl, Identifier, MatDecl, UnaryOp, VarDecl, Visitor
from src.parser import precedence_dict

class RenderVisitor(Visitor):
	"""This visitor that renders the AST using the minimum amount of parentheses possible."""

	def visit(self, root: Ast) -> None:
		root.accept(self)
		print('\n', end='')

	def _need_parenthesis(self, parent_op, node):
		if isinstance(node, (BinaryOp, UnaryOp)):
			return precedence_dict[parent_op][1] > precedence_dict[node.op][1]
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
		print(constant.value, end='')

	def visit_identifier(self, id: Identifier) -> None:
		print(id.name, end='')

	def visit_vardecl(self, vardecl: VarDecl) -> None:
		vardecl.name.accept(self)
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
		self._render_funcall(fundecl.name, fundecl.args)
		print(' = ', end='')
		fundecl.body.accept(self)

	def visit_funcall(self, funcall: FunCall) -> None:
		self._render_funcall(funcall.name, funcall.args)

	def visit_binaryop(self, binop: BinaryOp) -> None:
		left_parenthesis = self._need_parenthesis(binop.op, binop.left)
		right_parenthesis = self._need_parenthesis(binop.op, binop.right)
		self._render_grouped(binop.left, left_parenthesis)
		if binop.op != '*' or not (isinstance(binop.left, Constant) \
			and isinstance(binop.right, Identifier)):
			print(binop.op, end='')
		self._render_grouped(binop.right, right_parenthesis)

	def visit_unaryop(self, unop: UnaryOp) -> None:
		operand_parenthesis = self._need_parenthesis(unop.op, unop.right)
		print(unop.op, end='')
		self._render_grouped(unop.right, operand_parenthesis)

from src.ast import Ast, BinaryOp, Constant, FunCall, FunDecl, Identifier, MatDecl, UnaryOp, \
	VarDecl, Visitor

class RenderVisitor(Visitor):
	"""This visitor that renders the AST using the minimum amount of parentheses possible."""

	def __init__(self):
		self.res = ''

	def visit(self, node: Ast):
		node.accept(self)
		return self.res

	def _need_parentheses(self, parent: BinaryOp, child, assoc):
		return isinstance(child, (BinaryOp, UnaryOp)) \
			and (parent.get_precedence() > child.get_precedence() \
			or (parent.get_precedence() == child.get_precedence()
			and parent.get_associativity() == assoc))

	def _render_grouped(self, node, need_parenthesis):
		if need_parenthesis:
			self.res += '('
		node.accept(self)
		if need_parenthesis:
			self.res += ')'

	def _render_funcall(self, name, args):
		name.accept(self)
		self.res += '('
		for i, arg in enumerate(args):
			if i > 0:
				self.res += ', '
			arg.accept(self)
		self.res += ')'

	def visit_constant(self, constant: Constant):
		self.res += str(constant.value)

	def visit_identifier(self, id: Identifier):
		self.res += id.value

	def visit_vardecl(self, vardecl: VarDecl):
		vardecl.id.accept(self)
		self.res += ' = '
		vardecl.value.accept(self)

	def visit_matdecl(self, matdecl: MatDecl):
		self.res += '['
		for i, row in enumerate(matdecl.rows):
			if i > 0:
				self.res += '; '
			self.res += '['
			for j, cell in enumerate(row):
				if j > 0:
					self.res += ', '
				cell.accept(self)
			self.res += ']'
		self.res += ']'

	def visit_fundecl(self, fundecl: FunDecl):
		self._render_funcall(fundecl.id, fundecl.args)
		self.res += ' = '
		fundecl.body.accept(self)

	def visit_funcall(self, funcall: FunCall):
		self._render_funcall(funcall.id, funcall.args)

	def visit_binaryop(self, binop: BinaryOp):
		left_parentheses = self._need_parentheses(binop, binop.left, 'right')
		right_parentheses = self._need_parentheses(binop, binop.right, 'left')
		self._render_grouped(binop.left, left_parentheses)
		if binop.op != '*' or not (isinstance(binop.left, Constant) \
			and isinstance(binop.right, Identifier)):
			self.res += ' ' + binop.op + ' '
		self._render_grouped(binop.right, right_parentheses)

	def visit_unaryop(self, unop: UnaryOp):
		need_parentheses = isinstance(unop.right, (BinaryOp, UnaryOp)) \
			and unop.get_precedence() > unop.right.get_precedence()
		if unop.op == '-':
			self.res += '-'
		self._render_grouped(unop.right, need_parentheses)

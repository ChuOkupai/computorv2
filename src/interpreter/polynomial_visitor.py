from src.ast import Assign, Ast, BinaryOp, Constant, Identifier, Solve, UnaryOp, Visitor
from src.dtype import Polynomial
from src.interpreter import InvalidPolynomialError

class PolynomialVisitor(Visitor):
	"""Builds a polynomial from the AST."""

	def __init__(self):
		self.stack = []
		self.res = Polynomial()

	def _pop_term(self):
		if len(self.stack) < 2:
			self.stack.append(0)
		coeff, degree = self.stack
		self.res.add_coefficient(coeff, degree)
		self.stack = []

	def visit(self, node: Ast):
		node.accept(self)
		return self.res

	def visit_assign(self, assign: Assign):
		self.visit(assign.target)
		self._pop_term()
		lpolynomial = self.res
		self.res = Polynomial()
		self.visit(assign.value)
		self._pop_term()
		self.res = lpolynomial - self.res

	def visit_binaryop(self, bop: BinaryOp):
		if bop.op == '*' and isinstance(bop.left, Constant):
			self.visit(bop.left)
			if isinstance(bop.right, Identifier):
				self.visit(bop.right)
				return
			elif isinstance(bop.right, BinaryOp) and bop.right.op == '^':
				self.visit(bop.right)
				return
		elif bop.op == '^' and isinstance(bop.left, Identifier) \
			and isinstance(bop.right, Constant):
			if not isinstance(bop.right.value, int) or bop.right.value < 0:
				raise InvalidPolynomialError
			if not self.stack:
				self.stack.append(1)
			self.stack.append(bop.right.value)
			return
		elif bop.op == '+' or bop.op == '-':
			self.visit(bop.left)
			self._pop_term()
			self.visit(bop.right)
			if bop.op == '-':
				self.stack[0] = -self.stack[0]
			return
		raise InvalidPolynomialError

	def visit_command(self, _):
		raise InvalidPolynomialError

	def visit_constant(self, constant: Constant):
		if not isinstance(constant.value, (int, float)):
			raise InvalidPolynomialError
		self.stack.append(constant.value)

	def visit_funcall(self, _):
		raise InvalidPolynomialError

	def visit_identifier(self, _):
		if not self.stack:
			self.stack.append(1)
		self.stack.append(1)

	def visit_matdecl(self, _):
		raise InvalidPolynomialError

	def visit_solve(self, solve: Solve):
		solve.assign.accept(self)

	def visit_unaryop(self, unop: UnaryOp):
		self.visit(unop.right)
		if unop.op == '-':
			self.stack[0] = -self.stack[0]

from src.ast import Assign, Ast, BinaryOp, FunCall, Identifier, MatDecl, Solve, UnaryOp, Visitor
from src.interpreter import Context

class DependenciesVisitor(Visitor):
	"""Finds all dependencies of an expression."""

	def __init__(self, ctx: Context):
		self.ctx = ctx
		self.visited_functions = set()
		self.visited_variables = set()

	def get_user_defined_functions(self):
		return set(filter(lambda x: not self.ctx.is_builtin(x), self.visited_functions))

	def visit(self, n: Ast):
		n.accept(self)

	def visit_assign(self, assign: Assign):
		self.visit(assign.value)

	def visit_binaryop(self, binop: BinaryOp):
		self.visit(binop.left)
		self.visit(binop.right)

	def visit_constant(self, _):
		pass

	def visit_funcall(self, funcall: FunCall):
		self.visited_functions.add(funcall.id.value)
		[self.visit(arg) for arg in funcall.args]

	def visit_identifier(self, id: Identifier):
		self.visited_variables.add(id.value)

	def visit_matdecl(self, matdecl: MatDecl):
		[[self.visit(cell) for cell in row] for row in matdecl.rows]

	def visit_solve(self, solve: Solve):
		self.visit(solve.assign)

	def visit_unaryop(self, unop: UnaryOp):
		self.visit(unop.right)

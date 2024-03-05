from src.ast import Assign, Ast, BinaryOp, Constant, FunCall, Identifier, MatDecl, \
	Solve, UnaryOp, Visitor
from src.dtype import Matrix
from src.interpreter import Storage

def catch_exception(func):
	def wrapped(self, *args, **kwargs):
		try:
			return func(self, *args, **kwargs)
		except Exception:
			self.storage.reset_stack()
			raise
	return wrapped

class EvalVisitor(Visitor):
	"""Evaluates the AST using the given storage."""

	def __init__(self, storage: Storage):
		self.res = None
		self.storage = storage

	@catch_exception
	def visit(self, node: Ast):
		node.accept(self)
		return self.res

	def visit_assign(self, assign: Assign):
		if isinstance(assign.target, Identifier):
			self.storage.set_variable(assign.target.value, self.visit(assign.value))
		elif isinstance(assign.target, FunCall):
			raise NotImplementedError('function assignments are not supported yet')
		else:
			raise ValueError('cannot assign an expression to another expression')

	def visit_binaryop(self, binop: BinaryOp):
		self.res = binop.evaluate(self.visit(binop.left), self.visit(binop.right))

	def visit_constant(self, constant: Constant):
		self.res = constant.value

	def visit_funcall(self, funcall: FunCall):
		raise NotImplementedError('function calls are not supported yet')

	def visit_identifier(self, id: Identifier):
		self.res = self.storage.get_variable(id.value)

	def visit_matdecl(self, matdecl: MatDecl):
		self.res = Matrix([[self.visit(cell) for cell in row] for row in matdecl.rows])

	def visit_solve(self, solve: Solve):
		raise NotImplementedError('solve statements are not supported yet')

	def visit_unaryop(self, unop: UnaryOp):
		self.res = unop.evaluate(self.visit(unop.right))

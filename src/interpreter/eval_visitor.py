from src.ast import Ast, BinaryOp, Constant, FunCall, FunDecl, Identifier, MatDecl, \
	RenderVisitor, UnaryOp, VarDecl, Visitor
from src.dtype import Matrix
from src.interpreter import FunctionCheckVisitor, InvalidNumberOfArgumentsError, Storage

def catch_exception(func):
	def wrapped(self, *args, **kwargs):
		try:
			return func(self, *args, **kwargs)
		except Exception:
			self._abort_execution()
			raise
	return wrapped

def matrix_mul(a, b):
	if not isinstance(a, Matrix) or not isinstance(b, Matrix):
		raise TypeError('Matrix multiplication is only defined for matrices.')
	return a.matmul(b)

class EvalVisitor(Visitor):
	"""Evaluates the AST using the given storage."""

	binary_ops = {
		'+': lambda a, b: a + b,
		'/': lambda a, b: a / b,
		'**': matrix_mul,
		'%': lambda a, b: a % b,
		'*': lambda a, b: a * b,
		'^': lambda a, b: a ** b,
		'-': lambda a, b: a - b
	}

	unary_ops = {
		'-': lambda a: -a,
		'+': lambda a: a
	}

	def __init__(self, storage: Storage):
		self.res = None
		self.storage = storage

	def _abort_execution(self):
		self.storage.reset_stack()

	@catch_exception
	def visit(self, node: Ast):
		node.accept(self)
		return self.res

	def visit_constant(self, constant: Constant):
		self.res = constant.value

	def visit_identifier(self, id: Identifier):
		self.res = self.storage.get_variable(id.value)

	def visit_vardecl(self, vardecl: VarDecl):
		self.storage.set_variable(vardecl.id.value, self.visit(vardecl.value))

	def visit_matdecl(self, matdecl: MatDecl):
		self.res = Matrix([[self.visit(cell) for cell in row] for row in matdecl.rows])

	def visit_fundecl(self, fundecl: FunDecl):
		FunctionCheckVisitor(self.storage).visit(fundecl)
		self.storage.set_function(fundecl.id.value, fundecl)
		self.res = RenderVisitor().visit(fundecl)

	def visit_funcall(self, funcall: FunCall):
		id = funcall.id.value
		func = self.storage.get_function(id)
		if isinstance(func, FunDecl):
			if len(func.args) != len(funcall.args):
				raise InvalidNumberOfArgumentsError(id, len(func.args), len(funcall.args))
			self.storage.push_scope()
			for name, value in zip(func.args, funcall.args):
				self.visit(VarDecl(name, value))
			print(func.args)
			print(func.body)
			self.res = self.visit(func.body)
			self.storage.pop_scope()
		else:
			self.res = func(*[self.visit(arg) for arg in funcall.args])

	def visit_binaryop(self, binop: BinaryOp):
		self.res = self.binary_ops[binop.op](self.visit(binop.left), self.visit(binop.right))

	def visit_unaryop(self, unop: UnaryOp):
		self.res = self.unary_ops[unop.op](self.visit(unop.right))

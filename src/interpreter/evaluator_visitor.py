from src.ast import Assign, Ast, BinaryOp, Constant, FunCall, Identifier, MatDecl, \
	RenderVisitor, Solve, UnaryOp, Visitor
from src.dtype import Matrix
from src.interpreter import Context, FunctionCheckVisitor, FunctionStorage, \
	InvalidArgumentsLengthError, Context

def catch_exception(func):
	def wrapped(self, *args, **kwargs):
		try:
			return func(self, *args, **kwargs)
		except Exception:
			self.context.reset_stack()
			raise
	return wrapped

class EvaluatorVisitor(Visitor):
	"""Evaluates the AST using the given context."""

	def __init__(self, context: Context):
		self.res = None
		self.context = context

	@catch_exception
	def visit(self, node: Ast):
		node.accept(self)
		return self.res

	def visit_assign(self, assign: Assign):
		target = assign.target
		if isinstance(target, Identifier):
			self.context.set_variable(target.value, self.visit(assign.value))
		elif isinstance(target, FunCall):
			FunctionCheckVisitor(self.context).visit(assign)
			function_context = FunctionStorage(target.args, assign.value)
			self.context.set_function(target.id.value, function_context)
			self.res = RenderVisitor().visit(assign)
		else:
			raise ValueError('cannot assign an expression to another expression.')

	def visit_binaryop(self, binop: BinaryOp):
		self.res = binop.evaluate(self.visit(binop.left), self.visit(binop.right))

	def visit_constant(self, constant: Constant):
		self.res = constant.value

	def visit_funcall(self, funcall: FunCall):
		id = funcall.id.value
		f = self.context.get_function(id)
		if isinstance(f, FunctionStorage):
			if len(f.args) != len(funcall.args):
				raise InvalidArgumentsLengthError(id, len(f.args), len(funcall.args))
			self.context.push_scope()
			for name, value in zip(f.args, funcall.args):
				self.visit(Assign(name, value))
			self.res = self.visit(f.body)
			self.context.pop_scope()
		else:
			self.res = f(*[self.visit(arg) for arg in funcall.args])

	def visit_identifier(self, id: Identifier):
		self.res = self.context.get_variable(id.value)

	def visit_matdecl(self, matdecl: MatDecl):
		self.res = Matrix([[self.visit(cell) for cell in row] for row in matdecl.rows])

	def visit_solve(self, solve: Solve):
		raise NotImplementedError('solve statements are not supported yet.')

	def visit_unaryop(self, unop: UnaryOp):
		self.res = unop.evaluate(self.visit(unop.right))

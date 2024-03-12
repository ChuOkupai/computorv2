from copy import deepcopy
from src.ast import Assign, Ast, BinaryOp, Constant, FunCall, Identifier, MatDecl, \
	Solve, UnaryOp, Visitor
from src.dtype import Matrix
from src.interpreter import Context, FunctionStorage, \
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
		self.context = context
		self.res = None

	@catch_exception
	def visit(self, node: Ast):
		node.accept(self)
		return self.res

	def visit_assign(self, assign: Assign):
		target = assign.target
		assign.value = self.visit(assign.value)
		expr = assign.value
		if isinstance(target, Identifier):
			if not isinstance(expr, Constant):
				raise TypeError('The right-hand side of an assignment must be a constant.')
			self.context.set_variable(target.value, expr.value)
		elif isinstance(target, FunCall):
			function_context = FunctionStorage(target.args, expr)
			self.context.set_function(target.id.value, function_context)
		self.res = expr

	def visit_binaryop(self, bop: BinaryOp):
		print('type(bop.left):', type(bop.left))
		print('type(bop.right):', type(bop.right))
		bop.left = self.visit(bop.left)
		bop.right = self.visit(bop.right)
		print('type(bop.left):', type(bop.left))
		print('type(bop.right):', type(bop.right))
		if isinstance(bop.left, Constant) and isinstance(bop.right, Constant):
			self.res = Constant(bop.evaluate(bop.left.value, bop.right.value))
		else:
			self.res = bop

	def visit_constant(self, constant: Constant):
		self.res = constant

	def visit_funcall(self, funcall: FunCall):
		id = funcall.id.value
		f = self.context.get_function(id)
		if isinstance(f, FunctionStorage):
			if len(f.args) != len(funcall.args):
				raise InvalidArgumentsLengthError(id, len(f.args), len(funcall.args))
			args = [self.visit(arg) for arg in funcall.args]
			self.context.push_scope()
			for name, value in zip(f.args, args):
				self.visit(Assign(name, value))
			self.res = self.visit(f.body)
			self.context.pop_scope()
		else:
			args = [self.visit(arg) for arg in funcall.args]
			for i, arg in enumerate(args):
				if not isinstance(arg, Constant):
					raise TypeError(f'Argument {i} of function {id} is not a constant.')
			self.res = Constant(f(*[arg.value for arg in args]))

	def visit_identifier(self, id: Identifier):
		print('visit_identifier:', id)
		self.res = self.context.get_variable(id.value)
		print('self.res:', self.res)
		self.res = Constant(self.res) if self.res is not None else id
		print(repr(self.res))

	def visit_matdecl(self, matdecl: MatDecl):
		values = [[self.visit(cell) for cell in row] for row in matdecl.rows]
		if all(isinstance(cell, Constant) for row in values for cell in row):
			self.res = Constant(Matrix([[cell.value for cell in row] for row in values]))

	def visit_solve(self, solve: Solve):
		raise NotImplementedError('solve statements are not supported yet.')

	def visit_unaryop(self, unop: UnaryOp):
		unop.right = self.visit(unop.right)
		if isinstance(unop.right, Constant):
			self.res = unop.evaluate(unop.right)

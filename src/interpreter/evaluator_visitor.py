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
			self.ctx.reset_stack()
			raise
	return wrapped

class EvaluatorVisitor(Visitor):
	"""Evaluates the AST using the given context."""

	def __init__(self, ctx: Context):
		self.ctx = ctx
		self.res = None
		self.expand_functions = True

	@catch_exception
	def visit(self, node: Ast):
		node.accept(self)
		return self.res

	def visit_assign(self, assign: Assign):
		target = assign.target
		if isinstance(target, FunCall):
			old_expand_functions = self.expand_functions
			self.expand_functions = False
			self.ctx.push_scope(target.id.value)
			[self.ctx.set_variable(arg.value, arg) for arg in target.args]
		expr = deepcopy(self.visit(assign.value))
		if isinstance(target, Identifier):
			self.ctx.set_variable(target.value, expr)
		elif isinstance(target, FunCall):
			self.ctx.set_function(target.id.value, FunctionStorage(target.args, expr))
			self.ctx.pop_scope()
			self.expand_functions = old_expand_functions
		self.res = expr

	def visit_binaryop(self, bop: BinaryOp):
		bop.left = self.visit(bop.left)
		bop.right = self.visit(bop.right)
		self.res = bop
		if all(isinstance(e, Constant) for e in (bop.left, bop.right)):
			self.res = Constant(bop.evaluate(bop.left.value, bop.right.value))
		else:
			self.res = bop

	def visit_constant(self, constant: Constant):
		self.res = constant

	def visit_funcall(self, funcall: FunCall):
		funcall.args = [self.visit(arg) for arg in funcall.args]
		id = funcall.id.value
		f = self.ctx.get_function(id)
		if isinstance(f, FunctionStorage):
			if len(f.args) != len(funcall.args):
				raise InvalidArgumentsLengthError(id, len(f.args), len(funcall.args))
			self.ctx.push_scope(id)
			for name, value in zip(f.args, funcall.args):
				self.visit(Assign(name, value))
			self.res = self.visit(deepcopy(f.body))
			self.ctx.pop_scope()
			if not self.expand_functions and not isinstance(self.res, Constant):
				self.res = funcall
		elif f and all(isinstance(arg, Constant) for arg in funcall.args):
			self.res = Constant(f(*[arg.value for arg in funcall.args]))
		else:
			self.res = funcall

	def visit_identifier(self, id: Identifier):
		r = deepcopy(self.ctx.get_variable(id.value))
		if r:
			self.res = r if isinstance(r, Ast) else Constant(r)
		else:
			self.res = id

	def visit_matdecl(self, matdecl: MatDecl):
		values = [[self.visit(cell) for cell in row] for row in matdecl.rows]
		if all(isinstance(cell, Constant) for row in values for cell in row):
			self.res = Constant(Matrix([[cell.value for cell in row] for row in values]))

	def visit_solve(self, solve: Solve):
		assign = solve.assign
		assign.target = self.visit(assign.target)
		assign.value = self.visit(assign.value)
		raise NotImplementedError('solve statements are not supported yet.')

	def visit_unaryop(self, unop: UnaryOp):
		unop.right = self.visit(unop.right)
		if isinstance(unop.right, Constant):
			self.res = Constant(unop.evaluate(unop.right.value))

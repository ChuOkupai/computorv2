from copy import deepcopy
from src.ast import Assign, Ast, BinaryOp, Command, Constant, FunCall, Identifier, MatDecl, \
	Solve, UnaryOp, Visitor
from src.dtype import Matrix
from src.interpreter import Context, DependenciesVisitor, EquationSolverFactory, \
	FunctionStorage, InterpreterErrorGroup, PolynomialVisitor, RemovedFunctionError, \
	SystemCommandFactory

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
		if isinstance(target, Identifier):
			self.res = self.visit(assign.value)
			self.ctx.set_variable(target.value, self.res)
		elif isinstance(target, FunCall):
			id = target.id.value
			old_expand_functions = self.expand_functions
			self.expand_functions = False
			self.ctx.push_scope(id)
			[self.ctx.set_variable(arg.value, arg) for arg in target.args]
			self.res = self.visit(assign.value)
			self.ctx.pop_scope()
			dv = DependenciesVisitor(self.ctx)
			dv.visit(self.res)
			old_dependencies = set()
			fs = self.ctx.get_function(id)
			if fs and len(fs.args) != len(target.args):
				old_dependencies = self.ctx.get_functions_using_dependency(id)
			fs = FunctionStorage(target.args, self.res, dv.get_user_defined_functions())
			self.ctx.set_function(id, fs)
			self.expand_functions = old_expand_functions
			[self.ctx.unset_function(dep) for dep in old_dependencies]
			old_dependencies = [RemovedFunctionError(dep, id) for dep in old_dependencies]
			if old_dependencies:
				raise InterpreterErrorGroup(old_dependencies)

	def visit_binaryop(self, bop: BinaryOp):
		bop.left = self.visit(bop.left)
		bop.right = self.visit(bop.right)
		self.res = bop
		if all(isinstance(e, Constant) for e in (bop.left, bop.right)):
			self.res = Constant(bop.evaluate(bop.left.value, bop.right.value))
		else:
			self.res = bop

	def visit_command(self, cmd: Command):
		self.res = None
		SystemCommandFactory.create(self.ctx, cmd.args).execute()

	def visit_constant(self, constant: Constant):
		self.res = constant

	def visit_funcall(self, funcall: FunCall):
		funcall.args = [self.visit(arg) for arg in funcall.args]
		id = funcall.id.value
		f = self.ctx.get_function(id)
		if isinstance(f, FunctionStorage):
			self.ctx.push_scope(id)
			[self.visit(Assign(name, value)) for name, value in zip(f.args, funcall.args)]
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
		matdecl.rows = [[self.visit(cell) for cell in row] for row in matdecl.rows]
		if all(isinstance(cell, Constant) for row in matdecl.rows for cell in row):
			self.res = Constant(Matrix([[cell.value for cell in row] for row in matdecl.rows]))
		else:
			self.res = matdecl

	def visit_solve(self, solve: Solve):
		assign = solve.assign
		assign.target = self.visit(assign.target)
		assign.value = self.visit(assign.value)
		pv = PolynomialVisitor()
		p = pv.visit(solve)
		solver = EquationSolverFactory.create(p)
		r = solver.solve(p)
		if isinstance(r, list):
			r = Matrix([[int(x) if isinstance(x, float) and x % 1 == 0 else x for x in r]])
		elif isinstance(r, float) and r % 1 == 0:
			r = int(r)
		self.res = Constant(r)

	def visit_unaryop(self, unop: UnaryOp):
		unop.right = self.visit(unop.right)
		if isinstance(unop.right, Constant):
			self.res = Constant(unop.evaluate(unop.right.value))
		elif unop.op == '+':
			self.res = unop.right
		elif isinstance(unop.right, UnaryOp):
			self.res = unop.right.right
		else:
			self.res = unop

from src.ast import Assign, Ast, BinaryOp, Constant, FunCall, Identifier, MatDecl, Solve, \
	UnaryOp, Visitor
from src.interpreter import AssignExpressionError, BuiltInConstantError, BuiltInFunctionError, \
	Context, CyclicDependencyError, FunctionStorage, InterpreterErrorGroup, \
	InvalidArgumentsLengthError, MultipleDeclarationError, RequireIdentifierError, \
	UndefinedFunctionError, UndefinedVariableError, UnusedParameterError

class AnalyzerVisitor(Visitor):
	"""Performs a semantic analysis of the AST."""

	def __init__(self, ctx: Context):
		self.ctx = ctx
		self.assign_target_id = None
		self.detect_unknown_variables = False
		self.unused_variables = set()
		self.errors = []

	def _check_signature(self, args: list):
		func_args = []
		duplicates = set()
		for i, arg in enumerate(args):
			if not isinstance(arg, Identifier):
				self._push_error(RequireIdentifierError, i)
			elif arg.value not in self.unused_variables:
				func_args.append(arg)
				self.unused_variables.add(arg.value)
			elif arg.value not in duplicates:
				self._push_error(MultipleDeclarationError, arg)
				duplicates.add(arg.value)
		return func_args

	def _push_error(self, error_type: type, *args):
		self.errors.append(error_type(self.ctx.get_scope(), *args))

	def _raise_errors(self):
		if self.errors:
			errors = self.errors
			self.errors = []
			raise InterpreterErrorGroup(errors)

	def _visit_function(self, args: list, body: Ast):
		[self._visit(Assign(arg, Constant(None))) for arg in args]
		self._visit(body)

	def _visit(self, n):
		n.accept(self)

	def visit(self, n):
		self._visit(n)
		self._raise_errors()

	def visit_assign(self, assign: Assign):
		old_detect_unknown_variables = self.detect_unknown_variables
		self.detect_unknown_variables = True
		target = assign.target
		if isinstance(target, Identifier):
			self._visit(assign.value)
			if self.ctx.is_constant(target.value):
				self._push_error(BuiltInConstantError, target.value)
			if self.ctx.get_depth():
				self.ctx.set_variable(target.value, assign.value)
		elif isinstance(target, FunCall):
			self.assign_target_id = target.id.value
			self.ctx.push_scope(self.assign_target_id)
			self._visit_function(self._check_signature(target.args), assign.value)
			for arg in self.unused_variables:
				self._push_error(UnusedParameterError, arg)
			self.ctx.pop_scope()
			if self.ctx.is_builtin(self.assign_target_id):
				self._push_error(BuiltInFunctionError, self.assign_target_id)
			self.assign_target_id = None
		else:
			self._push_error(AssignExpressionError)
		self.detect_unknown_variables = old_detect_unknown_variables

	def visit_binaryop(self, binop: BinaryOp):
		self._visit(binop.left)
		self._visit(binop.right)

	def visit_constant(self, _):
		pass

	def visit_funcall(self, funcall: FunCall):
		id = funcall.id.value
		if id == self.assign_target_id:
			self._push_error(CyclicDependencyError)
			[self._visit(arg) for arg in funcall.args]
			return
		f = self.ctx.get_function(id)
		if not f:
			self._push_error(UndefinedFunctionError, id)
		[self._visit(arg) for arg in funcall.args]
		self.ctx.push_scope(id)
		if isinstance(f, FunctionStorage):
			if len(f.args) != len(funcall.args):
				self._push_error(InvalidArgumentsLengthError, len(f.args), len(funcall.args))
			self._visit_function(f.args, f.body)
		elif f and len(funcall.args) > 1:
			self._push_error(InvalidArgumentsLengthError, 1, len(funcall.args))
		self.ctx.pop_scope()

	def visit_identifier(self, id: Identifier):
		v = self.ctx.get_variable(id.value)
		if not v and self.detect_unknown_variables:
			self._push_error(UndefinedVariableError, id.value)
		if self.ctx.get_scope() == self.assign_target_id and id.value in self.unused_variables:
			self.unused_variables.remove(id.value)

	def visit_matdecl(self, matdecl: MatDecl):
		[[self._visit(cell) for cell in row] for row in matdecl.rows]

	def visit_solve(self, solve: Solve):
		assign = solve.assign
		self._visit(assign.target)
		self._visit(assign.value)

	def visit_unaryop(self, unop: UnaryOp):
		self._visit(unop.right)

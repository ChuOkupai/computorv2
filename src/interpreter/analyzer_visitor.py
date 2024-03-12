from src.ast import Assign, BinaryOp, Constant, FunCall, Identifier, MatDecl, UnaryOp, Visitor
from src.interpreter import AssignExpressionError, BuiltInConstantError, BuiltInFunctionError, \
	Context, CyclicDependencyError, FunctionStorage, InterpreterErrorGroup, \
	InvalidArgumentsLengthError, MultipleDeclarationError, RequireIdentifierError, \
	UndefinedFunctionError, UndefinedVariableError, UnusedParameterError

class AnalyzerVisitor(Visitor):
	"""Performs a semantic analysis of the AST."""

	def __init__(self, context: Context):
		self.context = context
		self.assign_target_id = None
		self.detect_unknowns = False
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
		self.errors.append(error_type(self.context.get_scope(), *args))

	def _raise_errors(self):
		if self.errors:
			errors = self.errors
			self.errors = []
			raise InterpreterErrorGroup(errors)

	def _visit(self, n):
		n.accept(self)

	def visit(self, n):
		self._visit(n)
		self._raise_errors()

	def visit_assign(self, assign: Assign):
		old_detect_unknowns = self.detect_unknowns
		self.detect_unknowns = True
		target = assign.target
		if isinstance(target, Identifier):
			self._visit(assign.value)
			if self.context.is_constant(target.value):
				self._push_error(BuiltInConstantError, target.value)
			if self.context.get_depth():
				self.context.set_variable(target.value, assign.value)
		elif isinstance(target, FunCall):
			self.assign_target_id = target.id.value
			self.context.push_scope(self.assign_target_id)
			fs = FunctionStorage(self._check_signature(target.args), assign.value)
			[self._visit(Assign(arg, Constant(None))) for arg in fs.args]
			self._visit(fs.body)
			for arg in self.unused_variables:
				self._push_error(UnusedParameterError, arg)
			self.context.pop_scope()
			if self.context.is_builtin(self.assign_target_id):
				self._push_error(BuiltInFunctionError, self.assign_target_id)
			self.assign_target_id = None
		else:
			self._push_error(AssignExpressionError)
		self.detect_unknowns = old_detect_unknowns

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
		f = self.context.get_function(id)
		if not f and self.detect_unknowns:
			self._push_error(UndefinedFunctionError, id)
		[self._visit(arg) for arg in funcall.args]
		self.context.push_scope(id)
		if isinstance(f, FunctionStorage):
			if len(f.args) != len(funcall.args):
				self._push_error(InvalidArgumentsLengthError, len(f.args), len(funcall.args))
			[self._visit(Assign(arg, Constant(None))) for arg in f.args]
			self._visit(f.body)
		elif f and len(funcall.args) > 1:
			self._push_error(InvalidArgumentsLengthError, 1, len(funcall.args))
		self.context.pop_scope()

	def visit_identifier(self, id: Identifier):
		v = self.context.get_variable(id.value)
		if not v and self.detect_unknowns:
			self._push_error(UndefinedVariableError, id.value)
		if self.context.get_scope() == self.assign_target_id and id.value in self.unused_variables:
			self.unused_variables.remove(id.value)

	def visit_matdecl(self, matdecl: MatDecl):
		[[self._visit(cell) for cell in row] for row in matdecl.rows]

	def visit_solve(self, _):
		raise NotImplementedError

	def visit_unaryop(self, unop: UnaryOp):
		self._visit(unop.right)

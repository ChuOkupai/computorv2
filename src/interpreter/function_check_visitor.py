from src.ast import Assign, BinaryOp, Constant, FunCall, Identifier, MatDecl, UnaryOp, Visitor
from src.interpreter import Context, CyclicDependencyError, FunctionStorage, \
	InterpreterErrorGroup, InvalidArgumentsLengthError, MultipleDeclarationError, \
	RequireIdentifierError, UnusedParameterError

class FunctionCheckVisitor(Visitor):
	"""Checks if the function declaration is correct."""

	def __init__(self, context: Context):
		self.context = context
		self.visited_functions = set()
		self.unused_variables = set()
		self.depth = 0
		self.errors = []

	def _check_signature(self, id: str, args: list):
		func_args = []
		duplicates = set()
		for i, arg in enumerate(args):
			if not isinstance(arg, Identifier):
				self.errors.append(RequireIdentifierError(id, i))
			elif arg.value not in self.unused_variables:
				func_args.append(arg)
				self.unused_variables.add(arg.value)
			elif arg.value not in duplicates:
				self.errors.append(MultipleDeclarationError(id, arg))
				duplicates.add(arg.value)
		return func_args

	def _visit_function(self, id: str, fs: FunctionStorage, args: list):
		self.context.push_scope()
		if len(args) < len(fs.args):
			args += [Constant(None)] * (len(fs.args) - len(args))
		[self.visit(Assign(name, value)) for name, value in zip(fs.args, args)]
		if len(args) > len(fs.args):
			[self.visit(arg) for arg in args[len(fs.args):]]
		self.depth += 1
		self.visited_functions.add(id)
		self.context.push_call(id)
		self.visit(fs.body)
		self.context.pop_call()
		self.visited_functions.remove(id)
		self.depth -= 1
		self.context.pop_scope()

	def visit(self, n):
		n.accept(self)

	def visit_assign(self, assign: Assign):
		target = assign.target
		if isinstance(target, Identifier):
			try:
				self.context.set_variable(target.value, self.visit(assign.value))
			except Exception as e:
				self.errors.append(e)
		elif isinstance(target, FunCall):
			id = target.id.value
			func_args = self._check_signature(id, target.args)
			fs = FunctionStorage(func_args, assign.value)
			self._visit_function(id, fs, [Constant(None)] * len(func_args))
			unused_args = [arg.value for arg in func_args if arg.value in self.unused_variables]
			self.errors += [UnusedParameterError(id, arg) for arg in unused_args]
			if len(self.errors):
				raise InterpreterErrorGroup(self.errors)

	def visit_binaryop(self, binop: BinaryOp):
		self.visit(binop.left)
		self.visit(binop.right)

	def visit_constant(self, _):
		pass

	def visit_funcall(self, funcall: FunCall):
		id = funcall.id.value
		f = None
		if id in self.visited_functions:
			self.errors.append(CyclicDependencyError(id))
		else:
			try:
				f = self.context.get_function(id)
			except Exception as e:
				self.errors.append(e)
		if isinstance(f, FunctionStorage):
			if len(f.args) != len(funcall.args):
				self.errors.append(InvalidArgumentsLengthError(id, len(f.args), len(funcall.args)))
			self._visit_function(id, f, funcall.args)
		else:
			if f and len(funcall.args) > 1:
				self.errors.append(InvalidArgumentsLengthError(id, 1, len(funcall.args)))
			[self.visit(arg) for arg in funcall.args]

	def visit_identifier(self, id: Identifier):
		try:
			self.context.get_variable(id.value)
		except Exception as e:
			self.errors.append(e)
		if self.depth < 2 and id.value in self.unused_variables:
			self.unused_variables.remove(id.value)

	def visit_matdecl(self, matdecl: MatDecl):
		[[self.visit(cell) for cell in row] for row in matdecl.rows]

	def visit_solve(self, _):
		raise NotImplementedError

	def visit_unaryop(self, unop: UnaryOp):
		self.visit(unop.right)

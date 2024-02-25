from src.ast import BinaryOp, FunCall, FunDecl, Identifier, MatDecl, UnaryOp, VarDecl, Visitor
from src.interpreter import CyclicDependencyError, InvalidNumberOfArgumentsError, \
	MultipleDeclarationError, RequiredIdentifierError, Storage, UnusedArgumentsError

class FunctionCheckVisitor(Visitor):
	"""Checks if the function declaration is valid."""

	def __init__(self, storage: Storage):
		self.storage = storage
		self.visited_function_ids = set()
		self.unused_variable_ids = set()
		self.depth = 0

	def _pop_scope(self, id: str):
		self.depth -= 1
		self.visited_function_ids.remove(id)
		self.storage.pop_scope()

	def _push_scope(self, id: str):
		self.storage.push_scope()
		self.visited_function_ids.add(id)
		self.depth += 1

	def visit(self, fundecl: FunDecl):
		fundecl.accept(self)

	def visit_constant(self, _):
		pass

	def visit_identifier(self, id: Identifier):
		self.storage.get_variable(id.value)
		if self.depth == 1 and id.value in self.unused_variable_ids:
			self.unused_variable_ids.remove(id.value)

	def visit_vardecl(self, vardecl: VarDecl):
		if vardecl.value:
			self.visit(vardecl.value)
		self.storage.set_variable(vardecl.id.value, None)

	def visit_matdecl(self, matdecl: MatDecl):
		[[self.visit(cell) for cell in row] for row in matdecl.rows]

	def visit_fundecl(self, fundecl: FunDecl):
		id = fundecl.id.value
		for arg in fundecl.args:
			if not isinstance(arg, Identifier):
				raise RequiredIdentifierError(id, arg)
			if arg.value in self.unused_variable_ids:
				raise MultipleDeclarationError(id, arg.value)
			self.unused_variable_ids.add(arg.value)
		self._push_scope(id)
		[self.visit(VarDecl(arg, None)) for arg in fundecl.args]
		self.visit(fundecl.body)
		self._pop_scope(id)
		unused_args = [arg.value for arg in fundecl.args if arg.value in self.unused_variable_ids]
		if unused_args:
			raise UnusedArgumentsError(id, unused_args)

	def visit_funcall(self, funcall: FunCall):
		id = funcall.id.value
		if id in self.visited_function_ids:
			raise CyclicDependencyError(id)
		func = self.storage.get_function(id)
		if isinstance(func, FunDecl):
			if len(func.args) != len(funcall.args):
				raise InvalidNumberOfArgumentsError(id, len(func.args), len(funcall.args))
			[self.visit(VarDecl(name, value)) for name, value in zip(func.args, funcall.args)]
			self._push_scope(id)
			self.visit(func.body)
			self._pop_scope(id)

	def visit_binaryop(self, binop: BinaryOp):
		self.visit(binop.left)
		self.visit(binop.right)

	def visit_unaryop(self, unop: UnaryOp):
		self.visit(unop.right)

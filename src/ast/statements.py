from src.ast import Ast
from src.ast.terminals import Identifier

class FunCall(Ast):
	"""Represents a function call statement."""

	def __init__(self, name: Identifier, args: list):
		self.name = name
		self.args = args

	def accept(self, visitor):
		return visitor.visit_funcall(self)

	def __repr__(self):
		name = repr(self.name)
		args = repr(self.args)
		return f"{self.__class__.__name__}({name}, {args})"

	def __str__(self):
		return f"{self.name}({', '.join(map(str, self.args))})"

class FunDecl(Ast):
	"""Represents a function declaration statement."""

	def __init__(self, name: Identifier, args: list, body: Ast):
		self.name = name
		self.args = args
		self.body = body

	def accept(self, visitor):
		visitor.visit_fundecl(self)

	def __repr__(self):
		name = repr(self.name)
		args = repr(self.args)
		body = repr(self.body)
		return f"{self.__class__.__name__}({name}, {args}, {body})"

	def __str__(self):
		return f"{self.name}({', '.join(map(str, self.args))}) = {self.body}"

class VarDecl(Ast):
	"""Represents a variable declaration statement."""

	def __init__(self, name: Identifier, value: Ast):
		self.name = name
		self.value = value

	def accept(self, visitor):
		visitor.visit_vardecl(self)

	def __repr__(self):
		name = repr(self.name)
		value = repr(self.value)
		return f"{self.__class__.__name__}({name}, {value})"

	def __str__(self):
		return f"{self.name} = {self.value}"

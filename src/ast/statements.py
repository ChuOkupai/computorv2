from src.ast import Ast
from src.ast.terminals import Identifier

class FunCall(Ast):
	"""Represents a function call statement."""

	def __init__(self, id: Identifier, args: list):
		self.id = id
		self.args = args

	def accept(self, visitor):
		return visitor.visit_funcall(self)

	def __repr__(self):
		id = repr(self.id)
		args = repr(self.args)
		return f"{self.__class__.__name__}({id}, {args})"

	def __str__(self):
		return f"{self.id}({', '.join(map(str, self.args))})"

class FunDecl(Ast):
	"""Represents a function declaration statement."""

	def __init__(self, id: Identifier, args: list, body: Ast):
		self.id = id
		self.args = args
		self.body = body

	def accept(self, visitor):
		visitor.visit_fundecl(self)

	def __repr__(self):
		id = repr(self.id)
		args = repr(self.args)
		body = repr(self.body)
		return f"{self.__class__.__name__}({id}, {args}, {body})"

	def __str__(self):
		return f"{self.id}({', '.join(map(str, self.args))}) = {self.body}"

class MatDecl(Ast):
	"""Represents a matrix declaration statement."""

	def __init__(self, rows: list):
		self.rows = rows

	def accept(self, visitor):
		visitor.visit_matdecl(self)

	def __repr__(self):
		rows = repr(self.rows)
		return f"{self.__class__.__name__}({rows})"

	def __str__(self):
		return f"[{';'.join(map(str, self.rows))}]"

class VarDecl(Ast):
	"""Represents a variable declaration statement."""

	def __init__(self, id: Identifier, value: Ast):
		self.id = id
		self.value = value

	def accept(self, visitor):
		visitor.visit_vardecl(self)

	def __repr__(self):
		id = repr(self.id)
		value = repr(self.value)
		return f"{self.__class__.__name__}({id}, {value})"

	def __str__(self):
		return f"{self.id} = {self.value}"

from src.ast import Ast, Identifier

class Assign(Ast):
	"""Represents an assignment statement."""

	def __init__(self, target: Ast, value: Ast):
		self.target = target
		self.value = value

	def accept(self, visitor):
		return visitor.visit_assign(self)

	def __repr__(self):
		return f"{self.__class__.__name__}({repr(self.target)}, {repr(self.value)})"

class FunCall(Ast):
	"""Represents a function call statement."""

	def __init__(self, id: Identifier, args: list):
		self.id = id
		self.args = args

	def accept(self, visitor):
		return visitor.visit_funcall(self)

	def __repr__(self):
		return f"{self.__class__.__name__}({repr(self.id)}, {repr(self.args)})"

class MatDecl(Ast):
	"""Represents a matrix declaration statement."""

	def __init__(self, rows: list):
		self.rows = rows

	def accept(self, visitor):
		visitor.visit_matdecl(self)

	def __repr__(self):
		return f"{self.__class__.__name__}({repr(self.rows)})"

class Solve(Ast):
	"""Represents a solve statement."""

	def __init__(self, assign: Assign):
		self.assign = assign

	def accept(self, visitor):
		visitor.visit_solve(self)

	def __repr__(self):
		return f"{self.__class__.__name__}({repr(self.assign)})"

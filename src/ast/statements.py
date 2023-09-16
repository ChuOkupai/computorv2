from src.ast import Ast

class FunCall(Ast):
	"""Represents a function call statement."""

	def __init__(self, lineno, col_offset, name, args):
		super().__init__(lineno, col_offset)
		self.name = name
		self.args = args

	def accept(self, visitor):
		return visitor.visit_funcall(self)

	def __repr__(self):
		return f"{self.__class__.__name__}({self.lineno}, {self.col_offset}, {self.name}, {self.args})"

	def __str__(self):
		return self.__repr__()

class FunDecl(Ast):
	"""Represents a function declaration statement."""

	def __init__(self, lineno, col_offset, name, args, body):
		super().__init__(lineno, col_offset)
		self.name = name
		self.args = args
		self.body = body

	def accept(self, visitor):
		return visitor.visit_fundecl(self)

	def __repr__(self):
		return f"{self.__class__.__name__}({self.lineno}, {self.col_offset}, {self.name}, {self.args}, {self.body})"

	def __str__(self):
		return self.__repr__()

class Sequence(Ast):
	"""Represents a sequence of statements."""

	def __init__(self, lineno, col_offset, statements):
		super().__init__(lineno, col_offset)
		self.statements = statements

	def accept(self, visitor):
		return visitor.visit_sequence(self)

	def __repr__(self):
		return f"{self.__class__.__name__}({self.lineno}, {self.col_offset}, {self.statements})"

	def __str__(self):
		return self.__repr__()

class VarDecl(Ast):
	"""Represents a variable declaration statement."""

	def __init__(self, lineno, col_offset, name, value):
		super().__init__(lineno, col_offset)
		self.name = name
		self.value = value

	def accept(self, visitor):
		return visitor.visit_vardecl(self)

	def __repr__(self):
		return f"{self.__class__.__name__}({self.lineno}, {self.col_offset}, {self.name}, {self.value})"

	def __str__(self):
		return self.__repr__()

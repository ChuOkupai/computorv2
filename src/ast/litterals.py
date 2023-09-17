from src.ast import Ast

class Constant(Ast):
	"""Represents a constant value."""

	def __init__(self, lineno, col_offset, value):
		super().__init__(lineno, col_offset)
		self.value = value
	
	def accept(self, visitor):
		return visitor.visit_litteral(self)
	
	def __repr__(self):
		return f"{self.__class__.__name__}({self.lineno}, {self.col_offset}, {self.value})"

	def __str__(self):
		return str(self.value)

class Variable(Ast):
	"""Represents a variable."""

	def __init__(self, lineno, col_offset, name):
		super().__init__(lineno, col_offset)
		self.name = name
	
	def accept(self, visitor):
		return visitor.visit_litteral(self)
	
	def __repr__(self):
		return f"{self.__class__.__name__}({self.lineno}, {self.col_offset}, {self.name})"

	def __str__(self):
		return self.name

from src.ast import Ast

class Constant(Ast):
	"""Represents a constant value."""

	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visit_constant(self)

	def __repr__(self):
		value = repr(self.value)
		return f"{self.__class__.__name__}({value})"

class Identifier(Ast):
	"""Represents a function or variable identifier."""

	def __init__(self, value: str):
		self.value = value

	def accept(self, visitor):
		visitor.visit_identifier(self)

	def __repr__(self):
		value = repr(self.value)
		return f"{self.__class__.__name__}({value})"

from abc import ABC, abstractmethod

class Ast(ABC):
	"""Represents an Abstract Syntax Tree node."""

	def __init__(self, lineno, col_offset):
		self.lineno = lineno
		self.col_offset = col_offset

	@abstractmethod
	def accept(self, visitor) -> None:
		pass

	def __repr__(self):
		return f"{self.__class__.__name__}({self.lineno}, {self.col_offset})"

	def __str__(self):
		return self.__repr__()

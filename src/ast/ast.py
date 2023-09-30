from abc import ABC, abstractmethod

class Ast(ABC):
	"""Represents an Abstract Syntax Tree node."""

	@abstractmethod
	def accept(self, visitor):
		pass

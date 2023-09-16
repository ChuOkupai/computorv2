from abc import ABC, abstractmethod

class Visitor(ABC):
	"""Represents a visitor for the AST."""

	# Constants

	@abstractmethod
	def visit_litteral(self, element: Litteral) -> None:
		pass

	# Statements

	@abstractmethod
	def visit_assign(self, element: Assign) -> None:
		pass

	@abstractmethod
	def visit_sequence(self, element: Sequence) -> None:
		pass

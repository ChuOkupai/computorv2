from abc import ABC, abstractmethod
from src.ast import BinaryOp, Constant, FunCall, FunDecl, Identifier, UnaryOp, VarDecl

class Visitor(ABC):
	"""Represents a visitor for the AST."""

	@abstractmethod
	def visit_constant(self, element: Constant) -> None:
		pass

	@abstractmethod
	def visit_identifier(self, element: Identifier) -> None:
		pass

	@abstractmethod
	def visit_vardecl(self, element: VarDecl) -> None:
		pass

	@abstractmethod
	def visit_fundecl(self, element: FunDecl) -> None:
		pass

	@abstractmethod
	def visit_funcall(self, element: FunCall) -> None:
		pass

	@abstractmethod
	def visit_binaryop(self, element: BinaryOp) -> None:
		pass

	@abstractmethod
	def visit_unaryop(self, element: UnaryOp) -> None:
		pass

from abc import ABC, abstractmethod
from src.ast import Assign, BinaryOp, Constant, FunCall, Identifier, MatDecl, Solve, UnaryOp

class Visitor(ABC):
	"""Represents a visitor for the AST."""

	@abstractmethod
	def visit_assign(self, assign: Assign) -> None:
		pass

	@abstractmethod
	def visit_binaryop(self, binop: BinaryOp) -> None:
		pass

	@abstractmethod
	def visit_constant(self, constant: Constant) -> None:
		pass

	@abstractmethod
	def visit_funcall(self, funcall: FunCall) -> None:
		pass

	@abstractmethod
	def visit_identifier(self, id: Identifier) -> None:
		pass

	@abstractmethod
	def visit_matdecl(self, matdecl: MatDecl) -> None:
		pass

	@abstractmethod
	def visit_solve(self, solve: Solve) -> None:
		pass

	@abstractmethod
	def visit_unaryop(self, unop: UnaryOp) -> None:
		pass

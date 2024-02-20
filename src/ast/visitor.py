from abc import ABC, abstractmethod
from src.ast import BinaryOp, Constant, FunCall, FunDecl, Identifier, MatDecl, UnaryOp, VarDecl

class Visitor(ABC):
	"""Represents a visitor for the AST."""

	@abstractmethod
	def visit_constant(self, constant: Constant) -> None:
		pass

	@abstractmethod
	def visit_identifier(self, id: Identifier) -> None:
		pass

	@abstractmethod
	def visit_vardecl(self, vardecl: VarDecl) -> None:
		pass

	@abstractmethod
	def visit_matdecl(self, matdecl: MatDecl) -> None:
		pass

	@abstractmethod
	def visit_fundecl(self, fundecl: FunDecl) -> None:
		pass

	@abstractmethod
	def visit_funcall(self, funcall: FunCall) -> None:
		pass

	@abstractmethod
	def visit_binaryop(self, binop: BinaryOp) -> None:
		pass

	@abstractmethod
	def visit_unaryop(self, unop: UnaryOp) -> None:
		pass

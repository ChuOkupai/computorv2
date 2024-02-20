from enum import Enum
from src.ast import Ast

class BinaryOp(Ast):
	"""Represents a binary operation."""

	def __init__(self, left: Ast, op: str, right: Ast):
		self.left = left
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visit_binaryop(self)

	def __repr__(self):
		left = repr(self.left)
		op = repr(self.op)
		right = repr(self.right)
		return f"{self.__class__.__name__}({left}, {op}, {right})"

	def __str__(self):
		return f"({self.left} {self.op} {self.right})"

class UnaryOp(Ast):
	"""Represents a unary operation."""

	def __init__(self, op: str, right: Ast):
		self.op = op
		self.right = right

	def accept(self, visitor):
		visitor.visit_unaryop(self)

	def __repr__(self):
		op = repr(self.op)
		right = repr(self.right)
		return f"{self.__class__.__name__}({op}, {right})"

	def __str__(self):
		return f"({self.op}{self.right})"

from enum import Enum
from src.ast import Ast

class BinaryOpType(Enum):
	"""Represents the type of a binary operation."""

	Add = 0
	Div = 1
	Mod = 2
	Mul = 3
	Pow = 4
	Sub = 5

class BinaryOp(Ast):
	"""Represents a binary operation."""

	def __init__(self, left: Ast, op: BinaryOpType, right: Ast):
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
		ops = ['+', '/', '%', '*', '^', '-']
		return f"({self.left} {ops[self.op.value]} {self.right})"

class UnaryOpType(Enum):
	"""Represents the type of a unary operation."""

	Neg = 0
	Pos = 1

class UnaryOp(Ast):
	"""Represents a unary operation."""

	def __init__(self, op: UnaryOpType, right: Ast):
		self.op = op
		self.right = right

	def accept(self, visitor):
		visitor.visit_unaryop(self)

	def __repr__(self):
		op = repr(self.op)
		right = repr(self.right)
		return f"{self.__class__.__name__}({op}, {right})"

	def __str__(self):
		ops = ['-', '+']
		return f"({ops[self.op.value]}{self.right})"

from src.parser import associativity_dict, precedence_dict
from src.ast import Ast

class BinaryOp(Ast):
	"""Represents a binary operation."""

	def __init__(self, left: Ast, op: str, right: Ast):
		self.left = left
		self.op = op
		self.right = right

	def _convert_to_token(self):
		symbol_to_token = {
			'+': 'ADD',
			'/': 'DIV',
			'**': 'MATMUL',
			'%': 'MOD',
			'*': 'MUL',
			'^': 'POW',
			'-': 'SUB'
		}
		return symbol_to_token[self.op]

	def accept(self, visitor):
		return visitor.visit_binaryop(self)

	def get_associativity(self):
		return associativity_dict[self._convert_to_token()]

	def get_precedence(self):
		return precedence_dict[self._convert_to_token()]

	def __repr__(self):
		left = repr(self.left)
		op = repr(self.op)
		right = repr(self.right)
		return f"{self.__class__.__name__}({left}, {op}, {right})"

class UnaryOp(Ast):
	"""Represents a unary operation."""

	def __init__(self, op: str, right: Ast):
		self.op = op
		self.right = right

	def _convert_to_token(self):
		return 'UADD' if self.op == '+' else 'USUB'

	def accept(self, visitor):
		visitor.visit_unaryop(self)

	def get_associativity(self):
		return associativity_dict[self._convert_to_token()]

	def get_precedence(self):
		return precedence_dict[self._convert_to_token()]

	def __repr__(self):
		op = repr(self.op)
		right = repr(self.right)
		return f"{self.__class__.__name__}({op}, {right})"

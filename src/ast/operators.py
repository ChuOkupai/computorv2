from src.parser import associativity_dict, precedence_dict
from src.ast import Ast
from src.dtype import Matrix

def matrix_mul(a, b):
	if not isinstance(a, Matrix) or not isinstance(b, Matrix):
		raise TypeError('Matrix multiplication is only defined for matrices.')
	return a.matmul(b)

class BinaryOp(Ast):
	"""Represents a binary operation."""

	binary_ops = {
		'+': lambda a, b: a + b,
		'/': lambda a, b: a / b,
		'**': matrix_mul,
		'%': lambda a, b: a % b,
		'*': lambda a, b: a * b,
		'^': lambda a, b: a ** b,
		'-': lambda a, b: a - b
	}

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

	def evaluate(self, left, right):
		return self.binary_ops[self.op](left, right)

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

	unary_ops = {
		'-': lambda a: -a,
		'+': lambda a: a
	}

	def __init__(self, op: str, right: Ast):
		self.op = op
		self.right = right

	def _convert_to_token(self):
		return 'UADD' if self.op == '+' else 'USUB'

	def accept(self, visitor):
		visitor.visit_unaryop(self)

	def evaluate(self, right):
		return self.unary_ops[self.op](right)

	def get_associativity(self):
		return associativity_dict[self._convert_to_token()]

	def get_precedence(self):
		return precedence_dict[self._convert_to_token()]

	def __repr__(self):
		op = repr(self.op)
		right = repr(self.right)
		return f"{self.__class__.__name__}({op}, {right})"

import math
from src.dtype import Complex, Matrix
from src.interpreter import FunctionStorage, Scope

def matrix_inv(m):
	if not isinstance(m, Matrix):
		raise TypeError('matrix inversion is only defined for matrices.')
	return m.inverse()

class Context:
	"""This class is used to store constants, variables, built-in functions and user-defined
	functions."""

	builtins = {
		'abs': abs,
		'cos': math.cos,
		'exp': math.exp,
		'identity': Matrix.identity,
		'inv': matrix_inv,
		'log': math.log,
		'ones': Matrix.ones,
		'sin': math.sin,
		'sqrt': math.sqrt,
		'tan': math.tan,
		'zeros': Matrix.zeros
	}

	constants = {
		'e': math.e,
		'i': Complex(0, 1),
		'inf': math.inf,
		'pi': math.pi,
		'tau': math.tau
	}

	def __init__(self):
		self.functions = {}
		self.scopes = [Scope(None, {})]

	def get_all_symbols(self):
		symbols = set(self.builtins.keys())
		symbols |= set(self.constants.keys())
		symbols |= set(self.functions.keys())
		symbols |= {k for k in self.scopes[-1].variables.keys()}
		return symbols

	def get_depth(self):
		return len(self.scopes) - 1

	def get_function(self, id: str):
		if id in self.functions:
			return self.functions[id]
		if self.is_builtin(id):
			return self.builtins[id]
		return None

	def get_functions_using_dependency(self, dependency_id: str):
		return {k for k, v in self.functions.items() if dependency_id in v.dependencies}

	def get_scope(self):
		return self.scopes[-1].id

	def get_variable(self, id: str):
		for s in reversed(self.scopes):
			if id in s.variables:
				return s.variables[id]
		if self.is_constant(id):
			return self.constants[id]
		return None

	def is_builtin(self, id: str):
		return id in self.builtins

	def is_constant(self, id: str):
		return id in self.constants

	def pop_scope(self):
		if len(self.scopes) == 1:
			raise IndexError('cannot pop the global scope.')
		self.scopes.pop()

	def push_scope(self, id: str):
		self.scopes.append(Scope(id, {}))

	def reset_stack(self):
		self.scopes = self.scopes[:1]

	def set_function(self, id: str, content: FunctionStorage):
		self.functions[id] = content

	def set_variable(self, id: str, value):
		self.scopes[-1].variables[id] = value

	def unset_function(self, id: str):
		self.functions.pop(id)

	def unset_variable(self, id: str):
		self.scopes[-1].variables.pop(id)

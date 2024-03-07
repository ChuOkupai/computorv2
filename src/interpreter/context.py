import math
from copy import copy
from src.dtype import Complex
from src.interpreter import BuiltInConstantError, BuiltInFunctionError, FunctionStorage, \
	UndefinedSymbolError

class Context:
	"""This class is used to store constants, variables, built-in functions and user-defined
	functions."""

	builtins = {
		'abs': abs,
		'cos': math.cos,
		'exp': math.exp,
		'log': math.log,
		'sin': math.sin,
		'sqrt': math.sqrt,
		'tan': math.tan
	}

	constants = {
		'e': math.e,
		'i': Complex(0, 1),
		'inf': math.inf,
		'nan': math.nan,
		'pi': math.pi,
		'tau': math.tau
	}

	def __init__(self):
		self.functions = {}
		self.variables = [{}]
		self.call_stack = [None]

	def get_function(self, name: str):
		if name in self.builtins:
			return self.builtins[name]
		if name in self.functions:
			return self.functions[name]
		raise UndefinedSymbolError(self.call_stack[-1], name)

	def get_variable(self, name: str):
		if name in self.constants:
			return copy(self.constants[name])
		for scope in reversed(self.variables):
			if name in scope:
				return copy(scope[name])
		raise UndefinedSymbolError(self.call_stack[-1], name)

	def pop_call(self):
		self.call_stack.pop()

	def pop_scope(self):
		self.variables.pop()

	def push_call(self, id: str):
		self.call_stack.append(id)

	def push_scope(self):
		self.variables.append({})

	def reset_stack(self):
		self.variables = self.variables[:1]
		self.call_stack = [None]

	def set_function(self, name: str, function_storage: FunctionStorage):
		if name in self.builtins:
			raise BuiltInFunctionError(self.call_stack[-1], name)
		self.functions[name] = function_storage

	def set_variable(self, name: str, value):
		if name in self.constants:
			raise BuiltInConstantError(self.call_stack[-1], name)
		self.variables[-1][name] = value

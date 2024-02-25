import math
from copy import copy
from src.ast import FunDecl
from src.dtype import Complex
from src.interpreter import BuiltInFunctionError, ConstantSymbolError, UndefinedSymbolError

class Storage:
	"""This class is used to store constants, variables, built-in functions and user-defined functions."""

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

	def get_function(self, name: str):
		if name in self.builtins:
			return self.builtins[name]
		if name in self.functions:
			return self.functions[name]
		raise UndefinedSymbolError(name)

	def get_variable(self, name: str):
		if name in self.constants:
			return copy(self.constants[name])
		for scope in reversed(self.variables):
			if name in scope:
				return copy(scope[name])
		raise UndefinedSymbolError(name)

	def pop_scope(self):
		self.variables.pop()

	def push_scope(self):
		self.variables.append({})

	def reset_stack(self):
		self.variables = self.variables[:1]

	def set_function(self, name: str, fundecl: FunDecl):
		if name in self.builtins:
			raise BuiltInFunctionError(name)
		self.functions[name] = fundecl

	def set_variable(self, name: str, value):
		if name in self.constants:
			raise ConstantSymbolError(name)
		self.variables[-1][name] = value

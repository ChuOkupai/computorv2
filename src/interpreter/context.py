import math
from src.dtype import Complex
from src.interpreter import BuiltInConstantError, BuiltInFunctionError, FunctionStorage, \
	InterpreterErrorGroup, UndefinedFunctionError, UndefinedVariableError

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
		'pi': math.pi,
		'tau': math.tau
	}

	def __init__(self):
		self.functions = {}
		self.variables = [{}]
		self.call_stack = [None]
		self.errors = []

	def get_function(self, name: str):
		if name in self.builtins:
			return self.builtins[name]
		if name in self.functions:
			return self.functions[name]
		self.push_error(UndefinedFunctionError, name)
		return None

	def get_variable(self, name: str):
		if name in self.constants:
			return self.constants[name]
		for scope in reversed(self.variables):
			if name in scope:
				return scope[name]
		self.push_error(UndefinedVariableError, name)
		return None

	def pop_call(self):
		self.call_stack.pop()

	def pop_errors(self):
		self.reset_stack()
		if self.errors:
			errors = self.errors
			self.errors = []
			raise InterpreterErrorGroup(errors)

	def pop_scope(self):
		self.variables.pop()

	def push_call(self, id: str):
		self.call_stack.append(id)

	def push_error(self, error_type: type, *args):
		self.errors.append(error_type(self.call_stack[-1], *args))

	def push_scope(self):
		self.variables.append({})

	def reset_stack(self):
		self.variables = self.variables[:1]
		self.call_stack = [None]

	def set_function(self, name: str, function_storage: FunctionStorage):
		if name in self.builtins:
			self.push_error(BuiltInFunctionError, name)
		else:
			self.functions[name] = function_storage

	def set_variable(self, name: str, value):
		if name in self.constants:
			self.push_error(BuiltInConstantError, name)
		else:
			self.variables[-1][name] = value

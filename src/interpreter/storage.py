import copy, math
from src.dtype import Complex

class Storage:
	"""Storage class for storing variables and functions."""

	def __init__(self):
		self.constants = {
			'e': math.e,
			'i': Complex(0, 1),
			'inf': math.inf,
			'nan': math.nan,
			'pi': math.pi,
			'tau': math.tau
		}
		self.variables = {}

	def is_constant(self, name: str):
		return name in self.constants

	def get_variable(self, name: str):
		if self.is_constant(name):
			return copy.deepcopy(self.constants[name])
		return self.variables.get(name, None)

	def set_variable(self, name: str, value):
		self.variables[name] = value

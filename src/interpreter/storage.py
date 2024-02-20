class Storage:
	"""Storage class for storing variables and functions."""

	def __init__(self):
		self.variables = {}

	def get_variable(self, name: str):
		return self.variables.get(name.lower(), None)

	def set_variable(self, name: str, value):
		self.variables[name.lower()] = value

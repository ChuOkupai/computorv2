class BuiltInFunctionError(SyntaxError):
	def __init__(self, id):
		super().__init__(f"function {id} is a built-in function.")

class ConstantSymbolError(SyntaxError):
	def __init__(self, id):
		super().__init__(f"symbol {id} is a constant.")

class CyclicDependencyError(SyntaxError):
	def __init__(self, id):
		super().__init__(f"found cyclic function call to {id}.")

class InvalidNumberOfArgumentsError(SyntaxError):
	def __init__(self, id, expected, actual):
		super().__init__(f"function {id} expects {expected} arguments, got {actual}.")

class MultipleDeclarationError(SyntaxError):
	def __init__(self, id, arg):
		super().__init__(f"function {id} has multiple declarations of argument {arg}.")

class RequiredIdentifierError(SyntaxError):
	def __init__(self, id, arg):
		super().__init__(f"function {id} expects an identifier as an argument, got {arg}.")

class UndefinedSymbolError(SyntaxError):
	def __init__(self, id):
		super().__init__(f"symbol {id} is not defined.")

class UnusedArgumentsError(SyntaxError):
	def __init__(self, id, unused_args):
		plural = 's' if len(unused_args) > 1 else ''
		unused_args = ', '.join(unused_args)
		super().__init__(f"function {id} has unused argument{plural}: {unused_args}.")

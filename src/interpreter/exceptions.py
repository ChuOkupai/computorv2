from src.ast import Identifier

class InterpreterError(RuntimeError):
	"""Base class for exceptions in the interpreter."""

	def __init__(self, scope_id: str, message: str):
		super().__init__(f"function {scope_id}: {message}." if scope_id else f'{message}.')

class InterpreterErrorGroup(Exception):
	"""Collection of errors during execution."""

	def __init__(self, errors: list):
		self.errors = errors

class CyclicDependencyError(InterpreterError):
	def __init__(self, scope_id: str):
		super().__init__(scope_id, "call results in an infinite loop")

class InvalidArgumentsLengthError(InterpreterError):
	def __init__(self, scope_id: str, expected: int, got: int):
		plural = 's' if expected > 1 else ''
		super().__init__(scope_id, f"expected {expected} argument{plural}, got {got}")

class MultipleDeclarationError(InterpreterError):
	def __init__(self, scope_id: str, arg: Identifier):
		super().__init__(scope_id, f"multiple declarations of parameter {arg.value}")

class RequireIdentifierError(InterpreterError):
	def __init__(self, scope_id: str, index: int):
		super().__init__(scope_id, f"expects an identifier for parameter {index + 1}")

class UnusedParameterError(InterpreterError):
	def __init__(self, scope_id: str, param: str):
		super().__init__(scope_id, f"unused parameter {param}")

class BuiltInConstantError(InterpreterError):
	def __init__(self, scope_id: str, id: str):
		super().__init__(scope_id, f"{id} is a built-in constant")

class BuiltInFunctionError(InterpreterError):
	def __init__(self, scope_id: str, id: str):
		super().__init__(scope_id, f"{id} is a built-in function")

class UndefinedSymbolError(InterpreterError):
	def __init__(self, scope_id: str, id: str):
		super().__init__(scope_id, f"{id} is not defined")

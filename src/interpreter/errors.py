from src.ast import Identifier

class CommandError(RuntimeError):
	"""Runtime error for commands."""

	def __init__(self, cmd: str, message: str):
		super().__init__(f"{cmd}: {message}.")

class InterpreterError(RuntimeError):
	"""Base class for exceptions in the interpreter."""

	def __init__(self, scope_id: str, message: str):
		super().__init__(f"function {scope_id}: {message}." if scope_id else f'{message}.')

class InterpreterErrorGroup(Exception):
	"""Collection of errors during execution."""

	def __init__(self, errors: list):
		self.errors = errors

class AssignExpressionError(InterpreterError):
	def __init__(self, scope_id: str):
		super().__init__(scope_id, "cannot assign to an expression")

class BuiltInConstantError(InterpreterError):
	def __init__(self, scope_id: str, id: str):
		super().__init__(scope_id, f"{id} is a built-in constant")

class BuiltInFunctionError(InterpreterError):
	def __init__(self, scope_id: str, id: str):
		super().__init__(scope_id, f"{id} is a built-in function")

class CyclicDependencyError(InterpreterError):
	def __init__(self, scope_id: str):
		super().__init__(scope_id, "call results in an infinite loop")

class InvalidArgumentsLengthError(InterpreterError):
	def __init__(self, scope_id: str, expected: int, got: int):
		plural = 's' if expected > 1 else ''
		super().__init__(scope_id, f"expected {expected} argument{plural}, got {got}")

class InvalidCommandError(InterpreterError):
	def __init__(self, cmd: str):
		super().__init__(None, f"{cmd}: invalid command")

class InvalidPolynomialDegreeError(InterpreterError):
	def __init__(self, degree: int):
		super().__init__(None, f"cannot solve polynomial of degree {degree}")

class InvalidPolynomialError(InterpreterError):
	def __init__(self):
		super().__init__(None, "invalid polynomial expression")

class MultipleDeclarationError(InterpreterError):
	def __init__(self, scope_id: str, arg: Identifier):
		super().__init__(scope_id, f"multiple declarations of parameter {arg.value}")

class RemovedFunctionError(InterpreterError):
	def __init__(self, id: str, call_id: str):
		super().__init__(None,
			f"function {id} has been removed due to an invalid function call to {call_id}")

class RequireIdentifierError(InterpreterError):
	def __init__(self, scope_id: str, index: int):
		super().__init__(scope_id, f"expects an identifier for parameter {index + 1}")

class TooManyEquationVariablesError(InterpreterError):
	def __init__(self, scope_id: str, expected: int, got: int):
		plural = 's' if expected > 1 else ''
		super().__init__(scope_id, f"expected {expected} equation variable{plural}, got {got}")

class UndefinedFunctionError(InterpreterError):
	def __init__(self, scope_id: str, id: str):
		super().__init__(scope_id, f"function {id} is not defined")

class UndefinedVariableError(InterpreterError):
	def __init__(self, scope_id: str, id: str):
		super().__init__(scope_id, f"variable {id} is not defined")

class UnusedParameterError(InterpreterError):
	def __init__(self, scope_id: str, param: str):
		super().__init__(scope_id, f"unused parameter {param}")

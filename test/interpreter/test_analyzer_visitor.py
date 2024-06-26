import unittest
from src.ast import Assign, BinaryOp, Command, Constant, FunCall, Identifier, MatDecl, Solve, \
	UnaryOp
from src.interpreter.errors import *
from src.interpreter import Context, FunctionStorage, AnalyzerVisitor

class TestAnalyzerVisitor(unittest.TestCase):
	"""This class checks if all exceptions are raised correctly."""

	def _assert_errors_raised(self, expected_error_types: list[type]):
		"""Assert that the given error types are raised."""
		with self.assertRaises(InterpreterErrorGroup) as e:
			AnalyzerVisitor(self.ctx).visit(self.ast)
		e = e.exception
		self.assertEqual(len(e.errors), len(expected_error_types))
		for err, et in zip(e.errors, expected_error_types):
			self.assertEqual(type(err), et)

	def setUp(self):
		self.ctx = Context()
		self.ast = Assign(None, None)

	def test_assign_expr_error(self):
		self.ast.target = BinaryOp(Identifier('x'), '+', Identifier('y'))
		self.ast.value = Identifier('x')
		self._assert_errors_raised([AssignExpressionError])

	def test_built_in_call(self):
		self.ast = FunCall(Identifier('log'), [Identifier('x')])
		AnalyzerVisitor(self.ctx).visit(self.ast)

	def test_built_in_constant_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x'), Identifier('pi')])
		self.ast.value = BinaryOp(Identifier('x'), '*', Identifier('pi'))
		self._assert_errors_raised([BuiltInConstantError])

	def test_built_in_function_error(self):
		self.ast.target = FunCall(Identifier('cos'), [Identifier('x')])
		self.ast.value = Identifier('x')
		self._assert_errors_raised([BuiltInFunctionError])

	def test_call_too_few_arguments(self):
		self.ctx.set_function('f', FunctionStorage([Identifier('x'), Identifier('y')], Identifier('x')))
		self.ast.target = FunCall(Identifier('g'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('f'), [Identifier('x')])
		self._assert_errors_raised([InvalidArgumentsLengthError])

	def test_call_too_many_arguments(self):
		self.ctx.set_function('f', FunctionStorage([Identifier('x')], Identifier('x')))
		self.ast.target = FunCall(Identifier('g'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('f'), [Identifier('x'), Identifier('x')])
		self._assert_errors_raised([InvalidArgumentsLengthError])

	def test_call_undefined_function(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('g'), [Identifier('x')])
		self._assert_errors_raised([UndefinedFunctionError])

	def test_call_undefined_variable(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = BinaryOp(Identifier('x'), '+', Identifier('y'))
		self._assert_errors_raised([UndefinedVariableError])

	def test_cyclic_dependency_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('f'), [Identifier('x')])
		self._assert_errors_raised([CyclicDependencyError])

	def test_invalid_arguments_length_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('cos'), [Identifier('x'), Identifier('x')])
		self._assert_errors_raised([InvalidArgumentsLengthError])

	def test_matdecl(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = MatDecl([[Constant(1), Identifier('x')]])
		AnalyzerVisitor(self.ctx).visit(self.ast)

	def test_multiple_declaration_error(self):
		self.ast.target = FunCall(Identifier('f'),
			[Identifier('x'), Identifier('x'), Identifier('y'), Identifier('x')])
		self.ast.value = BinaryOp(Identifier('x'), '+', Identifier('y'))
		self._assert_errors_raised([MultipleDeclarationError])

	def test_require_identifier_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x'), Constant(1)])
		self.ast.value = Identifier('x')
		self._assert_errors_raised([RequireIdentifierError])

	def test_solve(self):
		self.ast.target = Identifier('x')
		self.ast.value = Constant(1)
		AnalyzerVisitor(self.ctx).visit(Solve(self.ast))

	def test_too_many_equation_variables_error(self):
		self.ast.target = BinaryOp(Identifier('a'), '+', Identifier('b'))
		self.ast.value = Identifier('a')
		self.ast = Solve(self.ast)
		self._assert_errors_raised([TooManyEquationVariablesError])

	def test_unaryop(self):
		AnalyzerVisitor(self.ctx).visit(UnaryOp('-', Constant(1)))

	def test_undefined_function_error(self):
		self.ast = FunCall(Identifier('f'), [Identifier('x')])
		self._assert_errors_raised([UndefinedFunctionError])

	def test_unused_parameter_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x'), Identifier('y')])
		self.ast.value = Identifier('x')
		self._assert_errors_raised([UnusedParameterError])

	def test_multiple_errors(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x'), Identifier('y'), Constant(42), Identifier('y')])
		self.ast.value = FunCall(Identifier('g'), [BinaryOp(Identifier('x'), '+', Identifier('z'))])
		self._assert_errors_raised([RequireIdentifierError, MultipleDeclarationError,
			UndefinedFunctionError, UndefinedVariableError, UnusedParameterError])

	def test_command(self):
		AnalyzerVisitor(self.ctx).visit(Command(['foo', 'bar']))

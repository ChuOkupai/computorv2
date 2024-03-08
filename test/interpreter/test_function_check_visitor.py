import unittest
from src.ast import Assign, BinaryOp, Constant, FunCall, Identifier, MatDecl, Solve, UnaryOp
from src.interpreter.errors import *
from src.interpreter import Context, FunctionStorage, FunctionCheckVisitor as Fcv

class TestFunctionCheckVisitor(unittest.TestCase):
	"""This class checks if all exceptions are raised correctly."""

	def _assert_errors_raised(self, expected_error_types: list[type]):
		"""Assert that the given error types are raised."""
		with self.assertRaises(InterpreterErrorGroup) as e:
			Fcv(self.ctx).visit(self.ast)
		e = e.exception
		self.assertEqual(len(e.errors), len(expected_error_types))
		for err, et in zip(e.errors, expected_error_types):
			self.assertEqual(type(err), et)

	def setUp(self):
		self.ctx = Context()
		self.ast = Assign(None, None)

	def test_built_in_constant_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x'), Identifier('pi')])
		self.ast.value = BinaryOp(Identifier('x'), '*', Identifier('pi'))
		self._assert_errors_raised([BuiltInConstantError])

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
		self.ast.value = Identifier('x')
		Fcv(self.ctx).visit(self.ast)
		self.ast.value = FunCall(Identifier('f'), [Identifier('x')])
		self._assert_errors_raised([CyclicDependencyError])

	def test_invalid_arguments_length_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('cos'), [Identifier('x'), Identifier('x')])
		self._assert_errors_raised([InvalidArgumentsLengthError])

	def test_matdecl(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = MatDecl([[Constant(1), Identifier('x')]])
		Fcv(self.ctx).visit(self.ast)

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
		with self.assertRaises(NotImplementedError):
			Fcv(self.ctx).visit(Solve(None))

	def test_unaryop(self):
		Fcv(self.ctx).visit(UnaryOp('-', Constant(1)))

	def test_unused_parameter_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x'), Identifier('y')])
		self.ast.value = Identifier('x')
		self._assert_errors_raised([UnusedParameterError])

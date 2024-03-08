import math, unittest
from src.interpreter import BuiltInConstantError, BuiltInFunctionError, Context, \
	FunctionStorage, InterpreterErrorGroup, UndefinedFunctionError, UndefinedVariableError

class TestContext(unittest.TestCase):
	"""This class contains tests for the Context class."""

	def _assert_errors_raised(self, expected_error_types: list[type], func: callable, *args):
		"""Assert that the given error types are raised."""
		with self.assertRaises(InterpreterErrorGroup) as e:
			func(*args)
			self.ctx.pop_errors()
		e = e.exception
		self.assertEqual(len(e.errors), len(expected_error_types))
		for err, et in zip(e.errors, expected_error_types):
			self.assertEqual(type(err), et)

	def setUp(self):
		self.ctx = Context()

	def test_get_function(self):
		self.assertEqual(self.ctx.get_function('abs'), abs)

	def test_get_function_undefined(self):
		self._assert_errors_raised([UndefinedFunctionError], self.ctx.get_function, 'foo')

	def test_get_variable(self):
		self.assertEqual(self.ctx.get_variable('e'), math.e)

	def test_get_variable_undefined(self):
		self._assert_errors_raised([UndefinedVariableError], self.ctx.get_variable, 'foo')

	def test_set_function(self):
		self.ctx.set_function('f', None)
		self.assertEqual(self.ctx.get_function('f'), None)

	def test_set_function_builtin(self):
		self._assert_errors_raised([BuiltInFunctionError], self.ctx.set_function, 'abs', None)

	def test_set_variable(self):
		self.ctx.set_variable('y', 42)
		self.assertEqual(self.ctx.get_variable('y'), 42)

	def test_set_variable_constant(self):
		self._assert_errors_raised([BuiltInConstantError], self.ctx.set_variable, 'e', 42)

	def test_get_user_defined_function(self):
		f = FunctionStorage(None, None)
		self.ctx.set_function('f', f)
		self.assertEqual(self.ctx.get_function('f'), f)

	def test_get_user_defined_variable(self):
		self.ctx.set_variable('y', 42)
		self.assertEqual(self.ctx.get_variable('y'), 42)

	def test_scope_push_variable(self):
		self.ctx.push_scope()
		self.ctx.set_variable('x', 42)
		self.ctx.pop_scope()
		self._assert_errors_raised([UndefinedVariableError], self.ctx.get_variable, 'x')

	def test_scope_mask_variable(self):
		self.ctx.set_variable('x', 42)
		self.ctx.push_scope()
		self.ctx.set_variable('x', 43)
		self.assertEqual(self.ctx.get_variable('x'), 43)
		self.ctx.pop_scope()
		self.assertEqual(self.ctx.get_variable('x'), 42)

	def test_reset_stack(self):
		self.ctx.set_variable('x', 42)
		self.ctx.push_scope()
		self.ctx.set_variable('y', 43)
		self.ctx.reset_stack()
		self._assert_errors_raised([UndefinedVariableError], self.ctx.get_variable, 'y')

import math, unittest
from src.interpreter import BuiltInConstantError, BuiltInFunctionError, Context, \
	UndefinedSymbolError

class TestContext(unittest.TestCase):
	'''This class contains tests for the Context class.'''

	def setUp(self):
		self.s = Context()

	def test_get_function(self):
		self.assertEqual(self.s.get_function('abs'), abs)

	def test_get_function_undefined(self):
		with self.assertRaises(UndefinedSymbolError):
			self.s.get_function('foo')

	def test_get_variable(self):
		self.assertEqual(self.s.get_variable('e'), math.e)

	def test_get_variable_undefined(self):
		with self.assertRaises(UndefinedSymbolError):
			self.s.get_variable('foo')

	def test_set_function(self):
		self.s.set_function('f', None)
		self.assertEqual(self.s.get_function('f'), None)

	def test_set_function_builtin(self):
		with self.assertRaises(BuiltInFunctionError):
			self.s.set_function('abs', None)

	def test_set_variable(self):
		self.s.set_variable('y', 42)
		self.assertEqual(self.s.get_variable('y'), 42)

	def test_set_variable_constant(self):
		with self.assertRaises(BuiltInConstantError):
			self.s.set_variable('e', 42)

	def test_get_user_defined_function(self):
		self.s.set_function('f', None)
		self.assertEqual(self.s.get_function('f'), None)

	def test_get_user_defined_variable(self):
		self.s.set_variable('y', 42)
		self.assertEqual(self.s.get_variable('y'), 42)

	def test_scope_push_variable(self):
		self.s.push_scope()
		self.s.set_variable('x', 42)
		self.s.pop_scope()
		with self.assertRaises(UndefinedSymbolError):
			self.s.get_variable('x')

	def test_scope_mask_variable(self):
		self.s.set_variable('x', 42)
		self.s.push_scope()
		self.s.set_variable('x', 43)
		self.assertEqual(self.s.get_variable('x'), 43)
		self.s.pop_scope()
		self.assertEqual(self.s.get_variable('x'), 42)

	def test_reset_stack(self):
		self.s.set_variable('x', 42)
		self.s.push_scope()
		self.s.set_variable('y', 43)
		self.s.reset_stack()
		with self.assertRaises(UndefinedSymbolError):
			self.s.get_variable('y')

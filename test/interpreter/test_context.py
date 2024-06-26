import math, unittest
from src.dtype import Matrix
from src.interpreter import Context, FunctionStorage

class TestContext(unittest.TestCase):
	"""This class contains tests for the Context class."""

	def setUp(self):
		self.ctx = Context()

	def test_builtin_inv(self):
		inv = self.ctx.get_function('inv')
		with self.assertRaises(TypeError):
			inv(42)
		m = Matrix([[4, 3], [1, 1]])
		self.assertEqual(inv(m), Matrix([[1, -3], [-1, 4]]))

	def test_builtin_transpose(self):
		transpose = self.ctx.get_function('transpose')
		with self.assertRaises(TypeError):
			transpose(42)
		m = Matrix([[1, 2], [3, 4]])
		self.assertEqual(transpose(m), Matrix([[1, 3], [2, 4]]))

	def test_get_all_symbols(self):
		self.assertIsInstance(self.ctx.get_all_symbols(), set)

	def test_get_all_symbols_set_variable(self):
		self.assertFalse('foo' in self.ctx.get_all_symbols())
		self.ctx.set_variable('foo', 42)
		self.assertTrue('foo' in self.ctx.get_all_symbols())

	def test_get_depth(self):
		self.assertEqual(self.ctx.get_depth(), 0)

	def test_get_depth_nested(self):
		self.ctx.push_scope('foo')
		self.assertEqual(self.ctx.get_depth(), 1)
		self.ctx.push_scope('bar')
		self.assertEqual(self.ctx.get_depth(), 2)
		self.ctx.pop_scope()
		self.assertEqual(self.ctx.get_depth(), 1)

	def test_get_function(self):
		self.assertIsNone(self.ctx.get_function('f'))

	def test_get_function_builtin(self):
		self.assertEqual(self.ctx.get_function('abs'), abs)

	def test_get_function_user_defined(self):
		f = FunctionStorage([], None)
		self.ctx.set_function('f', f)
		self.assertEqual(self.ctx.get_function('f'), f)

	def test_get_functions_using_dependency(self):
		self.ctx.set_function('f', FunctionStorage([], None, {'x', 'y'}))
		self.ctx.set_function('g', FunctionStorage([], None, {'f'}))
		self.assertEqual(self.ctx.get_functions_using_dependency('f'), {'g'})
		self.assertEqual(self.ctx.get_functions_using_dependency('x'), {'f'})

	def test_get_scope(self):
		self.assertEqual(self.ctx.get_scope(), None)

	def test_get_variable(self):
		self.assertIsNone(self.ctx.get_variable('x'))

	def test_get_variable_between_scopes(self):
		self.ctx.push_scope('foo')
		self.ctx.set_variable('x', 42)
		self.ctx.push_scope('bar')
		self.assertEqual(self.ctx.get_variable('x'), 42)

	def test_get_variable_constant(self):
		self.assertEqual(self.ctx.get_variable('pi'), math.pi)

	def test_get_variable_user_defined(self):
		self.ctx.set_variable('y', 42)
		self.assertEqual(self.ctx.get_variable('y'), 42)

	def test_is_builtin(self):
		self.assertTrue(self.ctx.is_builtin('abs'))
		self.assertFalse(self.ctx.is_builtin('foo'))

	def test_is_constant(self):
		self.assertTrue(self.ctx.is_constant('pi'))
		self.assertFalse(self.ctx.is_constant('foo'))

	def test_pop_scope(self):
		with self.assertRaises(IndexError):
			self.ctx.pop_scope()

	def test_pop_scope_nested(self):
		self.ctx.push_scope('foo')
		self.ctx.push_scope('bar')
		self.ctx.pop_scope()
		self.assertEqual(self.ctx.get_scope(), 'foo')
		self.ctx.pop_scope()
		self.assertIsNone(self.ctx.get_scope())

	def test_push_scope(self):
		self.ctx.push_scope('foo')
		self.assertEqual(self.ctx.get_scope(), 'foo')

	def test_push_scope_nested(self):
		self.ctx.push_scope('foo')
		self.ctx.push_scope('bar')
		self.assertEqual(self.ctx.get_scope(), 'bar')

	def test_reset_stack(self):
		self.ctx.reset_stack()
		self.assertIsNone(self.ctx.get_scope())

	def test_reset_stack_with_scope(self):
		self.ctx.push_scope('foo')
		self.ctx.reset_stack()
		self.assertIsNone(self.ctx.get_scope())

	def test_set_function(self):
		self.ctx.set_function('f', None)
		self.assertEqual(self.ctx.get_function('f'), None)

	def test_set_function_builtin(self):
		self.ctx.set_function('abs', None)
		self.assertEqual(self.ctx.get_function('abs'), None)

	def test_set_variable(self):
		self.ctx.set_variable('y', 42)
		self.assertEqual(self.ctx.get_variable('y'), 42)

	def test_set_variable_constant(self):
		self.ctx.set_variable('e', 42)
		self.assertEqual(self.ctx.get_variable('e'), 42)

	def test_set_variable_on_scope(self):
		self.ctx.push_scope('test')
		self.ctx.set_variable('x', 42)
		self.assertEqual(self.ctx.get_variable('x'), 42)
		self.ctx.pop_scope()
		self.assertIsNone(self.ctx.get_variable('x'))

	def test_set_variable_on_scope_nested(self):
		self.ctx.push_scope('foo')
		self.ctx.set_variable('x', 42)
		self.ctx.push_scope('bar')
		self.ctx.set_variable('x', 43)
		self.assertEqual(self.ctx.get_variable('x'), 43)
		self.ctx.pop_scope()
		self.assertEqual(self.ctx.get_variable('x'), 42)
		self.ctx.pop_scope()
		self.assertIsNone(self.ctx.get_variable('x'))

	def test_scope_push_variable(self):
		self.ctx.push_scope('test')
		self.ctx.set_variable('x', 42)
		self.ctx.pop_scope()
		self.assertIsNone(self.ctx.get_variable('x'))

	def test_unset_function(self):
		self.ctx.set_function('f', None)
		self.ctx.unset_function('f')
		self.assertIsNone(self.ctx.get_function('f'))

	def test_unset_variable(self):
		self.ctx.set_variable('y', 42)
		self.ctx.unset_variable('y')
		self.assertIsNone(self.ctx.get_variable('y'))

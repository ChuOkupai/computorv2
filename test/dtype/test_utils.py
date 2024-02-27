import unittest
from src.dtype import Complex, is_close, is_literal, try_cast_as_int

class TestUtils(unittest.TestCase):
	"""This class contains tests for the utils module."""

	def test_is_close(self):
		self.assertTrue(is_close(1.0, 1.0))
		self.assertTrue(is_close(1.0, 1.0 + 1e-10))
		self.assertFalse(is_close(1.0, 1.0 + 1e-8))
		self.assertTrue(is_close(-1.0, -1.0))
		self.assertTrue(is_close(-1.0, -1.0 + 1e-10))
		self.assertFalse(is_close(-1.0, -1.0 + 1e-8))
		self.assertFalse(is_close(-1.0, 1.0))
		self.assertFalse(is_close(1.0, -1.0))
		self.assertTrue(is_close(Complex(1.0, 1.0), Complex(1.0, 1.0)))
		self.assertTrue(is_close(Complex(1.0, 1.0), Complex(1.0 + 1e-10, 1.0)))
		self.assertFalse(is_close(Complex(1.0, 1.0), Complex(1.0 + 1e-8, 1.0)))

	def test_is_literal(self):
		self.assertTrue(is_literal(1))
		self.assertTrue(is_literal(1.0))
		self.assertTrue(is_literal(Complex(1, 1)))
		self.assertTrue(is_literal(Complex(1.0, 1.0)))
		self.assertTrue(is_literal(Complex(1, 2)))
		self.assertFalse(is_literal('x'))
		self.assertFalse(is_literal([1, 2, 3]))
		self.assertFalse(is_literal((1, 2, 3)))
		self.assertFalse(is_literal({1, 2, 3}))
		self.assertFalse(is_literal({1: 2, 3: 4}))
		self.assertFalse(is_literal(None))

	def test_try_cast_as_int(self):
		self.assertEqual(try_cast_as_int(1), 1)
		self.assertEqual(try_cast_as_int(1.0), 1)
		self.assertEqual(try_cast_as_int(1.5), 1.5)
		self.assertEqual(try_cast_as_int(Complex(1, 1)), Complex(1, 1))
		self.assertEqual(try_cast_as_int('test'), 'test')

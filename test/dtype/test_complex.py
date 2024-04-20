import unittest
from src.dtype import Complex, Matrix

class TestComplex(unittest.TestCase):
	'''This class contains tests for the Complex class.'''

	def test_init(self):
		self.assertEqual(str(Complex()), '0i')
		self.assertEqual(str(Complex(1)), '1 + 0i')
		self.assertEqual(str(Complex(0, 1)), 'i')
		self.assertEqual(str(Complex(2, 3)), '2 + 3i')
		self.assertEqual(str(Complex(2, -3)), '2 - 3i')
		self.assertEqual(str(Complex(0, -3)), '-3i')

	def test_abs(self):
		self.assertEqual(abs(Complex(0, 1)), 1)
		self.assertEqual(abs(Complex(1, 2)), 2.23606797749979)
		self.assertEqual(abs(Complex(1, -2)), 2.23606797749979)

	def test_add(self):
		self.assertEqual(str(Complex(1, 2) + Complex(3, 4)), '4 + 6i')
		self.assertEqual(str(Complex(1, 2) + 3), '4 + 2i')
		self.assertEqual(str(Complex(1, 2) + 1.5), '2.5 + 2i')

	def test_add_matrix(self):
		c = Complex(1, 2)
		m = Matrix([[1, 2], [3, 4]])
		self.assertEqual(str(c + m), '[[2 + 2i, 3 + 2i]; [4 + 2i, 5 + 2i]]')

	def test_eq(self):
		self.assertEqual(Complex(1, 2), Complex(1, 2))
		self.assertEqual(Complex(1, 0), 1)

	def test_mod(self):
		with self.assertRaises(TypeError):
			Complex() % 1

	def test_mul(self):
		self.assertEqual(str(Complex(1, 2) * Complex(3, 4)), '-5 + 10i')
		self.assertEqual(str(Complex(1, 2) * 3), '3 + 6i')
		self.assertEqual(str(Complex(1, 2) * 1.5), '1.5 + 3i')

	def test_mul_matrix(self):
		c = Complex(1, 2)
		m = Matrix([[1, 2], [3, 4]])
		self.assertEqual(str(c * m), '[[1 + 2i, 2 + 4i]; [3 + 6i, 4 + 8i]]')

	def test_ne(self):
		self.assertNotEqual(Complex(1, 0), Complex(2, 0))
		self.assertNotEqual(Complex(1, 2), Complex(1, 3))
		self.assertNotEqual(Complex(1, 0), 2)
		self.assertNotEqual(Complex(1, 0), 'a')

	def test_neg(self):
		self.assertEqual(str(-Complex(0, 1)), '-i')
		self.assertEqual(str(-Complex(1, 2)), '-1 - 2i')
		self.assertEqual(str(-Complex(1, -2)), '-1 + 2i')

	def test_pos(self):
		self.assertEqual(str(+Complex(0, 0)), '0i')
		self.assertEqual(str(+Complex(1, 0)), '1 + 0i')
		self.assertEqual(str(+Complex(0, 1)), 'i')
		self.assertEqual(str(+Complex(1, 2)), '1 + 2i')
		self.assertEqual(str(+Complex(1, -2)), '1 - 2i')

	def test_pow(self):
		self.assertEqual(str(Complex(1, 2) ** 0), '1 + 0i')
		self.assertEqual(str(Complex(0, 0) ** 1), '0i')
		self.assertEqual(str(Complex(1, 2) ** 1), '1 + 2i')
		self.assertEqual(str(Complex(0, 1) ** 2), '-1 + 0i')
		self.assertEqual(str(Complex(1, 2) ** Complex(3, 4)), '0.129009594074467 + 0.03392409290517014i')

	def test_radd(self):
		self.assertEqual(str(3 + Complex(1, 2)), '4 + 2i')
		self.assertEqual(str(1.5 + Complex(1, 2)), '2.5 + 2i')

	def test_repr(self):
		self.assertEqual(repr(Complex()), 'Complex()')
		self.assertEqual(repr(Complex(1)), 'Complex(1)')
		self.assertEqual(repr(Complex(0, 1)), 'Complex(0, 1)')
		self.assertEqual(repr(Complex(1, 2)), 'Complex(1, 2)')
		self.assertEqual(repr(Complex(1, -2)), 'Complex(1, -2)')
		self.assertEqual(repr(Complex(-3)), 'Complex(-3)')
		self.assertEqual(repr(Complex(0, -3)), 'Complex(0, -3)')
		self.assertEqual(repr(Complex(-4, -5)), 'Complex(-4, -5)')

	def test_rmod(self):
		with self.assertRaises(TypeError):
			1 % Complex()

	def test_rmul(self):
		self.assertEqual(str(3 * Complex(1, 2)), '3 + 6i')
		self.assertEqual(str(1.5 * Complex(1, 2)), '1.5 + 3i')

	def test_rpow(self):
		self.assertEqual(str(1 ** Complex(0, 1)), '1 + 0i')
		self.assertEqual(str(1.5 ** Complex(1, 2)), '1.0332365865926958 + 1.0873923653062287i')
		self.assertRaises(ZeroDivisionError, Complex(1, 2).__rpow__, 0)

	def test_rsub(self):
		self.assertEqual(str(3 - Complex(1, 2)), '2 - 2i')
		self.assertEqual(str(1.5 - Complex(1, 2)), '0.5 - 2i')

	def test_rtruediv(self):
		self.assertEqual(str(8 / Complex(64, 32)), '0.1 - 0.05i')
		self.assertEqual(str(1.5 / Complex(1, 2)), '0.3 - 0.6i')

	def test_str(self):
		self.assertEqual(str(Complex()), '0i')
		self.assertEqual(str(Complex(1)), '1 + 0i')
		self.assertEqual(str(Complex(0, 1)), 'i')
		self.assertEqual(str(Complex(1, 2)), '1 + 2i')
		self.assertEqual(str(Complex(1, -2)), '1 - 2i')
		self.assertEqual(str(Complex(-3)), '-3 + 0i')
		self.assertEqual(str(Complex(0, -3)), '-3i')
		self.assertEqual(str(Complex(-4, -5)), '-4 - 5i')

	def test_sub(self):
		self.assertEqual(str(Complex(1, 2) - Complex(3, 4)), '-2 - 2i')
		self.assertEqual(str(Complex(1, 2) - 3), '-2 + 2i')
		self.assertEqual(str(Complex(1, 2) - 1.5), '-0.5 + 2i')

	def test_sub_matrix(self):
		c = Complex(1, 2)
		m = Matrix([[1, 2], [3, 4]])
		self.assertEqual(str(c - m), '[[2i, -1 + 2i]; [-2 + 2i, -3 + 2i]]')

	def test_truediv(self):
		self.assertEqual(str(Complex(1, 2) / Complex(3, 4)), '0.44 + 0.08i')
		self.assertEqual(str(Complex(1, 2) / 2), '0.5 + i')
		self.assertEqual(str(Complex(28, 21) / 3.5), '8 + 6i')

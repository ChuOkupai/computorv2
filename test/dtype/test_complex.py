import unittest
from src.dtype import Complex

class TestComplex(unittest.TestCase):
	"""This class contains tests for the Complex class."""

	def test_construct(self):
		self.assertEqual(str(Complex()), "0i")
		self.assertEqual(str(Complex(1)), "1 + 0i")
		self.assertEqual(str(Complex(2, 3)), "2 + 3i")
		self.assertEqual(str(Complex(2, -3)), "2 - 3i")
		self.assertEqual(str(Complex(0, -3)), "-3i")
		self.assertRaises(TypeError, Complex, "a")
		self.assertRaises(TypeError, Complex, 1, "a")
		self.assertRaises(OverflowError, Complex, int('1' + '0' * 309))

	def test_add(self):
		self.assertEqual(str(Complex(1, 2) + Complex(3, 4)), "4 + 6i")
		self.assertEqual(str(Complex(1, 2) + 3), "4 + 2i")
		self.assertEqual(str(Complex(1, 2) + 1.5), "2.5 + 2i")
		self.assertRaises(TypeError, Complex(1, 2).__add__, "a")

	def test_iadd(self):
		c = Complex(1, 2)
		c += Complex(3, 4)
		self.assertEqual(str(c), "4 + 6i")
		c += 3
		self.assertEqual(str(c), "7 + 6i")
		self.assertRaises(TypeError, Complex(1, 2).__iadd__, "a")

	def test_radd(self):
		self.assertEqual(str(3 + Complex(1, 2)), "4 + 2i")
		self.assertEqual(str(1.5 + Complex(1, 2)), "2.5 + 2i")
		self.assertRaises(TypeError, Complex(1, 2).__radd__, "a")

	def test_sub(self):
		self.assertEqual(str(Complex(1, 2) - Complex(3, 4)), "-2 - 2i")
		self.assertEqual(str(Complex(1, 2) - 3), "-2 + 2i")
		self.assertEqual(str(Complex(1, 2) - 1.5), "-0.5 + 2i")
		self.assertRaises(TypeError, Complex(1, 2).__sub__, "a")

	def test_isub(self):
		c = Complex(1, 2)
		c -= Complex(3, 4)
		self.assertEqual(str(c), "-2 - 2i")
		c -= 3
		self.assertEqual(str(c), "-5 - 2i")
		self.assertRaises(TypeError, Complex(1, 2).__isub__, "a")

	def test_rsub(self):
		self.assertEqual(str(3 - Complex(1, 2)), "2 - 2i")
		self.assertEqual(str(1.5 - Complex(1, 2)), "0.5 - 2i")
		self.assertRaises(TypeError, Complex(1, 2).__rsub__, "a")

	def test_mul(self):
		self.assertEqual(str(Complex(1, 2) * Complex(3, 4)), "-5 + 10i")
		self.assertEqual(str(Complex(1, 2) * 3), "3 + 6i")
		self.assertEqual(str(Complex(1, 2) * 1.5), "1.5 + 3i")
		self.assertRaises(TypeError, Complex(1, 2).__mul__, "a")

	def test_imul(self):
		c = Complex(1, 2)
		c *= Complex(3, 4)
		self.assertEqual(str(c), "-5 + 10i")
		c *= 3
		self.assertEqual(str(c), "-15 + 30i")
		self.assertRaises(TypeError, Complex(1, 2).__imul__, "a")

	def test_rmul(self):
		self.assertEqual(str(3 * Complex(1, 2)), "3 + 6i")
		self.assertEqual(str(1.5 * Complex(1, 2)), "1.5 + 3i")
		self.assertRaises(TypeError, Complex(1, 2).__rmul__, "a")

	def test_div(self):
		self.assertEqual(str(Complex(1, 2) / Complex(3, 4)), "0.44 + 0.08i")
		self.assertEqual(str(Complex(1, 2) / 2), "0.5 + i")
		self.assertEqual(str(Complex(28, 21) / 3.5), "8 + 6i")
		self.assertRaises(TypeError, Complex(1, 2).__truediv__, "a")

	def test_idiv(self):
		c = Complex(1, 2)
		c /= Complex(3, 4)
		self.assertEqual(str(c), "0.44 + 0.08i")
		c /= 2
		self.assertEqual(str(c), "0.22 + 0.04i")
		self.assertRaises(TypeError, Complex(1, 2).__itruediv__, "a")

	def test_rdiv(self):
		self.assertEqual(str(8 / Complex(64, 32)), "0.1 - 0.05i")
		self.assertEqual(str(1.5 / Complex(1, 2)), "0.3 - 0.6i")
		self.assertRaises(TypeError, Complex(1, 2).__rtruediv__, "a")

	def test_neg(self):
		self.assertEqual(str(-Complex()), "0i")
		self.assertEqual(str(-Complex(1)), "-1 + 0i")
		self.assertEqual(str(-Complex(0, 1)), "-i")
		self.assertEqual(str(-Complex(1, 2)), "-1 - 2i")
		self.assertEqual(str(-Complex(1, -2)), "-1 + 2i")

	def test_pos(self):
		self.assertEqual(str(+Complex()), "0i")
		self.assertEqual(str(+Complex(1)), "1 + 0i")
		self.assertEqual(str(+Complex(0, 1)), "i")
		self.assertEqual(str(+Complex(1, 2)), "1 + 2i")
		self.assertEqual(str(+Complex(1, -2)), "1 - 2i")

	def test_abs(self):
		self.assertEqual(abs(Complex()), 0)
		self.assertEqual(abs(Complex(1)), 1)
		self.assertEqual(abs(Complex(0, 1)), 1)
		self.assertEqual(abs(Complex(1, 2)), 2.23606797749979)
		self.assertEqual(abs(Complex(1, -2)), 2.23606797749979)

	def test_pow(self):
		self.fail(NotImplementedError)

	def test_ipow(self):
		self.fail(NotImplementedError)

	def test_rpow(self):
		self.fail(NotImplementedError)

	def test_eq(self):
		self.assertEqual(Complex(), Complex())
		self.assertEqual(Complex(1), Complex(1))
		self.assertEqual(Complex(1, 2), Complex(1, 2))
		self.assertEqual(Complex(1), 1)

	def test_ne(self):
		self.assertNotEqual(Complex(), Complex(1))
		self.assertNotEqual(Complex(1), Complex(2))
		self.assertNotEqual(Complex(1, 2), Complex(1, 3))
		self.assertNotEqual(Complex(1), 2)
		self.assertNotEqual(Complex(1), "a")

	def test_hash(self):
		self.assertEqual(hash(Complex()), hash(Complex()))
		self.assertEqual(hash(Complex(1)), hash(Complex(1)))
		self.assertEqual(hash(Complex(1, 2)), hash(Complex(1, 2)))

	def test_repr(self):
		self.assertEqual(repr(Complex()), "Complex()")
		self.assertEqual(repr(Complex(1)), "Complex(1)")
		self.assertEqual(repr(Complex(1.5, 2)), "Complex(1.5, 2)")
		self.assertEqual(repr(Complex(1, 2.5)), "Complex(1, 2.5)")
		self.assertEqual(repr(Complex(1, -2)), "Complex(1, -2)")

from src.dtype import Complex, Matrix
import unittest

class TestMatrix(unittest.TestCase):
	"""This class contains tests for the Matrix class."""

	def test_identity(self):
		m = Matrix.identity(3)
		self.assertEqual(m.values, [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
		self.assertEqual(m.shape, (3, 3))

	def test_ones(self):
		m = Matrix.ones(2, 3)
		self.assertEqual(m.values, [[1., 1., 1.], [1., 1., 1.]])
		self.assertEqual(m.shape, (2, 3))

	def test_zeros(self):
		m = Matrix.zeros(3, 2)
		self.assertEqual(m.values, [[0., 0.], [0., 0.], [0., 0.]])
		self.assertEqual(m.shape, (3, 2))

	def test_init(self):
		m = Matrix([[1., 2., 3.], [4., 5., 6.]])
		self.assertEqual(m.values, [[1., 2., 3.], [4., 5., 6.]])
		self.assertEqual(m.shape, (2, 3))

	def test_init_complex(self)	:
		m = Matrix([[Complex(), Complex(1)], [Complex(2, 3), Complex(4, 5)]])
		self.assertEqual(m.values, [[Complex(), Complex(1)], [Complex(2, 3), Complex(4, 5)]])
		self.assertEqual(m.shape, (2, 2))

	def test_init_complex_promotion(self):
		m = Matrix([[Complex(1), 2], [3, Complex(4)]])
		self.assertEqual(m.values, [[Complex(1), Complex(2)], [Complex(3), Complex(4)]])
		self.assertEqual(m.shape, (2, 2))

	def test_init_float_promotion(self):
		m = Matrix([[1, 2], [3.5, 4]])
		self.assertEqual(m.values, [[1., 2.], [3.5, 4.]])
		self.assertEqual(m.shape, (2, 2))

	def test_init_mixed_promotion(self):
		m = Matrix([[1, 2.4], [Complex(3), 4]])
		self.assertEqual(m.values, [[Complex(1), Complex(2.4)], [Complex(3), Complex(4)]])
		self.assertEqual(m.shape, (2, 2))

	def test_init_invalid_shape(self):
		with self.assertRaises(ValueError):
			Matrix([[1, 2], [3, 4, 6]])

	def test_init_invalid_type(self):
		with self.assertRaises(ValueError):
			Matrix([[1, 2], [3, 'oops']])

	def test_init_invalid_literal(self):
		with self.assertRaises(ValueError):
			Matrix([['x', 2], [3, 4]])

	def test_inverse(self):
		u = Matrix.identity(3)
		v = u.inverse()
		self.assertEqual(v.values, u.values)

		u *= 2
		v = u.inverse()
		self.assertEqual(v.values, [[0.5, 0., 0.], [0., 0.5, 0.], [0., 0., 0.5]])

		u = Matrix([[8., 5., -2.], [4., 7., 20.], [7., 6., 1.]])
		v = u.inverse()
		expectedValues = [[0.649425287, 0.097701149, -0.655172414], [-0.781609195, -0.126436782, 0.965517241], [0.143678161, 0.074712644, -0.206896552]]
		for i in range(3):
			for j in range(3):
				self.assertAlmostEqual(v.values[i][j], expectedValues[i][j])

	def test_inverse_complex(self):
		u = Matrix([[Complex(0, -1), Complex(1)], [Complex(2), Complex()]])
		expectedValues = [[Complex(), Complex(0.5)], [Complex(1), Complex(0, 0.5)]]
		v = u.inverse()
		for i in range(2):
			for j in range(2):
				self.assertEqual(v.values[i][j], expectedValues[i][j])

	def test_inverse_not_square(self):
		u = Matrix([[1., 2.], [3., 4.], [5., 6.]])
		with self.assertRaises(ValueError):
			u.inverse()

	def test_inverse_non_invertible(self):
		u = Matrix([[-5., 0., 2.], [1., -2., 3.], [6., -2., 1.]])
		with self.assertRaises(ValueError):
			u.inverse()

	def test_matmul(self):
		u = Matrix.identity(2)
		v = u.matmul(u)
		self.assertEqual(v.values, [[1., 0.], [0., 1.]])

		v = Matrix([[2., 1.], [4., 2.]])
		w = u.matmul(v)
		self.assertEqual(w.values, [[2., 1.], [4., 2.]])

		u = Matrix([[3., -5.], [6., 8.]])
		w = u.matmul(v)
		self.assertEqual(w.values, [[-14., -7.], [44., 22.]])

	def test_matmul_invalid_shape(self):
		u = Matrix([[1., 2.], [3., 4.]])
		v = Matrix([[1., 2.], [3., 4.], [5., 6.]])
		with self.assertRaises(ValueError):
			u.matmul(v)

	def test_transpose(self):
		u = Matrix([[1., 2.], [3., 4.]])
		v = u.transpose()
		self.assertEqual(v.values, [[1., 3.], [2., 4.]])

		u = Matrix([[3., 4., 5.], [6., 7., 8.]])
		v = u.transpose()
		self.assertEqual(v.values, [[3., 6.], [4., 7.], [5., 8.]])

	def test_add(self):
		u = Matrix([[1., 2.], [3., 4.]])
		v = Matrix([[7., 4.], [-2., 2.]])
		expectedValues = [[8., 6.], [1., 6.]]
		w = u + v
		self.assertEqual(w.values, expectedValues)

	def test_add_scl(self):
		u = Matrix([[1., 2.], [3., 4.]])
		expectedValues = [[3., 4.], [5., 6.]]
		v = u + 2
		self.assertEqual(v.values, expectedValues)

	def test_eq(self):
		m = Matrix([[1., 2.], [3., 4.]])
		self.assertEqual(m, m)

	def test_mod(self):
		m = Matrix([[7, 4], [3, 10]]) % 3
		self.assertEqual(m.values, [[1, 1], [0, 1]])

	def test_mod_scl(self):
		m = Matrix([[1., 2.], [3., 4.]])
		self.assertEqual((m % 2).values, [[1., 0.], [1., 0.]])

	def test_mul(self):
		u = Matrix([[1., 2.], [3., 4.]])
		v = Matrix([[7., 4.], [-2., 2.]])
		expectedValues = [[7., 8.], [-6., 8.]]
		w = u * v
		self.assertEqual(w.values, expectedValues)

	def test_mul_scl(self):
		u = Matrix([[1., 2.], [3., 4.]])
		expectedValues = [[2., 4.], [6., 8.]]
		v = u * 2
		self.assertEqual(v.values, expectedValues)

	def test_ne(self):
		m = Matrix([[1., 2.], [3., 4.]])
		self.assertNotEqual(m, Matrix([[1., 2.], [3., 5.]]))
		self.assertNotEqual(m, 1)

	def test_neg(self):
		m = Matrix([[1., 2.], [3., 4.]])
		self.assertEqual((-m).values, [[-1., -2.], [-3., -4.]])

	def test_pos(self):
		m = Matrix([[1., 2.], [3., 4.]])
		self.assertEqual((+m).values, [[1., 2.], [3., 4.]])

	def test_pow(self):
		m = Matrix([[1., 2.], [3., 4.]])
		self.assertEqual(m ** 0, Matrix.identity(2))
		self.assertEqual(Matrix([[1, 2], [3, 4]]) ** 0, Matrix.identity(2, dtype=int))
		self.assertEqual(Matrix([[Complex(1, 2), Complex(3, 4)], [Complex(5, 6), Complex(7, 8)]]) ** 0, Matrix.identity(2, dtype=Complex))
		self.assertEqual(m ** 1, m)
		self.assertEqual(m ** 2, m.matmul(m))

	def test_pow_invalid_shape(self):
		m = Matrix([[1., 2.], [3., 4.], [5., 6.]])
		with self.assertRaises(ValueError):
			m ** 2

	def test_pow_invalid_exponent(self):
		m = Matrix([[1., 2.], [3., 4.]])
		with self.assertRaises(TypeError):
			m ** 1.5

	def test_pow_negative_exponent(self):
		m = Matrix([[1., 2.], [3., 4.]])
		with self.assertRaises(ValueError):
			m ** -1

	def test_radd(self):
		u = Matrix([[1., 2.], [3., 4.]])
		expectedValues = [[8., 9.], [10., 11.]]
		v = 7 + u
		self.assertEqual(v.values, expectedValues)

	def test_repr(self):
		self.assertEqual(repr(Matrix([[1, 2], [3, 4]])), 'Matrix([[1, 2], [3, 4]])')
		self.assertEqual(repr(Matrix([[1., 2.], [3., 4.]])), 'Matrix([[1.0, 2.0], [3.0, 4.0]])')
		self.assertEqual(repr(Matrix.identity(2)), 'Matrix([[1.0, 0.0], [0.0, 1.0]])')
		self.assertEqual(repr(Matrix([[Complex(), Complex(1)]])), 'Matrix([[Complex(), Complex(1)]])')
		self.assertEqual(repr(Matrix([[Complex(1, 2)], [Complex(3, 4)]])), 'Matrix([[Complex(1, 2)], [Complex(3, 4)]])')

	def test_rmod(self):
		with self.assertRaises(TypeError):
			1 % Matrix.identity(3)

	def test_rmul(self):
		u = Matrix([[1., 2.], [3., 4.]])
		expectedValues = [[2., 4.], [6., 8.]]
		v = 2 * u
		self.assertEqual(v.values, expectedValues)

	def test_rpow(self):
		with self.assertRaises(TypeError):
			1 ** Matrix.identity(3)

	def test_rsub(self):
		u = Matrix([[1., 2.], [3., 4.]])
		expectedValues = [[6., 5.], [4., 3.]]
		v = 7 - u
		self.assertEqual(v.values, expectedValues)

	def test_rtruediv(self):
		with self.assertRaises(TypeError):
			1 / Matrix.identity(3)

	def test_str(self):
		self.assertEqual(str(Matrix([[1, 2], [3, 4]])), '[[1, 2]; [3, 4]]')
		self.assertEqual(str(Matrix([[1., 2.], [3., 4.]])), '[[1.0, 2.0]; [3.0, 4.0]]')
		self.assertEqual(str(Matrix.identity(2)), '[[1.0, 0.0]; [0.0, 1.0]]')
		self.assertEqual(str(Matrix([[Complex(), Complex(1)]])), '[[0i, 1 + 0i]]')
		self.assertEqual(str(Matrix([[Complex(1, 2)], [Complex(3, 4)]])), '[[1 + 2i]; [3 + 4i]]')

	def test_sub(self):
		u = Matrix([[1., 2.], [3., 4.]])
		v = Matrix([[7., 4.], [-2., 2.]])
		expectedValues = [[-6., -2.], [5., 2.]]
		w = u - v
		self.assertEqual(w.values, expectedValues)

	def test_sub_scl(self):
		u = Matrix([[1., 2.], [3., 4.]])
		expectedValues = [[-1., 0.], [1., 2.]]
		v = u - 2
		self.assertEqual(v.values, expectedValues)

	def test_truediv(self):
		u = Matrix([[1., 2.], [3., 4.]])
		v = u / 2
		self.assertEqual(v.values, [[0.5, 1.], [1.5, 2.]])

	def test_truediv_invalid_type(self):
		u = Matrix([[1., 2.], [3., 4.]])
		with self.assertRaises(ValueError):
			u / Matrix.identity(3)

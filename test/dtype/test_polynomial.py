from src.dtype import Polynomial
import unittest

class TestPolynomial(unittest.TestCase):
	"""This class contains tests for the Polynomial class."""

	def test_init(self):
		p = Polynomial()
		self.assertEqual(p.terms, {})

	def test_init_with_terms(self):
		p = Polynomial({0: 42})
		self.assertEqual(p.terms, {0: 42})

	def test_add(self):
		p1 = Polynomial({0: 1, 1: 2})
		p2 = Polynomial({0: 2, 1: 3})
		p = p1 + p2
		self.assertEqual(p.terms, {0: 3, 1: 5})

	def test_eq(self):
		p1 = Polynomial({0: 1, 1: 2})
		p2 = Polynomial({0: 1, 1: 2})
		self.assertEqual(p1, p2)
		p2 = Polynomial({0: 1, 1: 3})
		self.assertNotEqual(p1, p2)

	def test_neg(self):
		p = Polynomial({0: 1, 1: 2})
		self.assertEqual(-p, Polynomial({0: -1, 1: -2}))

	def test_repr(self):
		p = Polynomial({0: 1, 1: 2})
		self.assertEqual(repr(p), 'Polynomial({0: 1, 1: 2})')

	def test_str(self):
		p = Polynomial({0: 1, 1: 2})
		self.assertEqual(str(p), '{0: 1, 1: 2}')

	def test_sub(self):
		p1 = Polynomial({0: 1, 1: 2})
		p2 = Polynomial({0: 2, 1: 3})
		p = p1 - p2
		self.assertEqual(p.terms, {0: -1, 1: -1})

	def test_add_coefficient(self):
		p = Polynomial()
		p.add_coefficient(2, 1)
		self.assertEqual(p.terms, {1: 2})
		p.add_coefficient(3, 1)
		self.assertEqual(p.terms, {1: 5})
		p.add_coefficient(-4, 1)
		self.assertEqual(p.terms, {1: 1})
		p.add_coefficient(2, 3)
		self.assertEqual(p.terms, {1: 1, 3: 2})
		p.add_coefficient(-1, 1)
		self.assertEqual(p.terms, {3: 2})

	def test_get_coefficient(self):
		p = Polynomial({1: 2})
		self.assertEqual(p.get_coefficient(1), 2)
		self.assertEqual(p.get_coefficient(2), 0)

	def test_get_degree(self):
		p = Polynomial({1: 2})
		self.assertEqual(p.get_degree(), 1)
		p = Polynomial()
		self.assertEqual(p.get_degree(), 0)

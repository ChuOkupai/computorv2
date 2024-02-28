import unittest
from src import *
from src.parser import parse

class TestParser(unittest.TestCase):
	"""This class contains tests for the parser."""

	def test_constant(self):
		self.assertEqual(repr(parse('1')), 'Constant(1)')
		self.assertEqual(repr(parse('1.0')), 'Constant(1.0)')
		self.assertEqual(repr(parse('1.0e-3')), 'Constant(0.001)')

	def test_variable(self):
		self.assertEqual(repr(parse('x')), "Identifier('x')")
		self.assertEqual(repr(parse('X')), "Identifier('X')")
		self.assertEqual(repr(parse('longVariableName')), "Identifier('longVariableName')")

	def test_matrix(self):
		self.assertEqual(repr(parse('[[1, 2]; [3, 4]]')), 'MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])')
		self.assertEqual(repr(parse('[[1, 2, 3]; [4, 5, 6]; [7, 8, 9]]')), 'MatDecl([[Constant(1), Constant(2), Constant(3)], [Constant(4), Constant(5), Constant(6)], [Constant(7), Constant(8), Constant(9)]])')

	def test_invalid_variable(self):
		with self.assertRaises(SyntaxError):
			parse('var1')

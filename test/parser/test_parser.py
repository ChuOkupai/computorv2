import unittest
from src import *
from src.parser import parse

class TestParser(unittest.TestCase):
	"""This class contains tests for the parser."""

	def test_assign_int(self):
		self.assertEqual(repr(parse('varA = 2')), "Assign(Identifier('varA'), Constant(2))")

	def test_assign_float(self):
		self.assertEqual(repr(parse('varB = 4.242')),
			"Assign(Identifier('varB'), Constant(4.242))")

	def test_assign_float_negative(self):
		self.assertEqual(repr(parse('varC = -4.3')),
			"Assign(Identifier('varC'), UnaryOp('-', Constant(4.3)))")

	def test_assign_complex(self):
		self.assertEqual(repr(parse('varA = 2*i + 3')),
			"Assign(Identifier('varA'), BinaryOp(BinaryOp(Constant(2), '*', Identifier('i')), '+', Constant(3)))")

	def test_assign_complex_negative(self):
		self.assertEqual(repr(parse('varB =  -4i - 4')),
			"Assign(Identifier('varB'), BinaryOp(UnaryOp('-', BinaryOp(Constant(4), '*', Identifier('i'))), '-', Constant(4)))")

	def test_assign_matrix(self):
		self.assertEqual(repr(parse('varC = [[2,3];[4,3]]')),
			"Assign(Identifier('varC'), MatDecl([[Constant(2), Constant(3)], [Constant(4), Constant(3)]]))")

	def test_assign_function(self):
		self.assertEqual(repr(parse('funA(x) = 2x + 1')),
			"Assign(FunCall(Identifier('funA'), [Identifier('x')]), BinaryOp(BinaryOp(Constant(2), '*', Identifier('x')), '+', Constant(1)))")

	def test_assign_function_multiple_args(self):
		self.assertEqual(repr(parse('funB(x, y) = x * y')),
			"Assign(FunCall(Identifier('funB'), [Identifier('x'), Identifier('y')]), BinaryOp(Identifier('x'), '*', Identifier('y')))")

	def test_compute(self):
		self.assertEqual(repr(parse('2 * 21 = ?')),
			"BinaryOp(Constant(2), '*', Constant(21))")

	def test_compute_function(self):
		self.assertEqual(repr(parse('funA(2) = ?')),
			"FunCall(Identifier('funA'), [Constant(2)])")

	def test_compute_eof(self):
		with self.assertRaises(EOFError):
			parse('a + 2 =')

	def test_solve(self):
		self.assertEqual(repr(parse('funA(x) = y ?')),
			"Solve(Assign(FunCall(Identifier('funA'), [Identifier('x')]), Identifier('y')))")

	def test_invalid_variable(self):
		with self.assertRaises(SyntaxError):
			parse('var1 = 2')

import unittest
from src.parser import parse

class TestParser(unittest.TestCase):
	"""This class contains tests for the parser."""

	def test_assign_int(self):
		self.assertEqual(repr(parse('varA = 2')), "Assign(Identifier('vara'), Constant(2))")

	def test_assign_float(self):
		self.assertEqual(repr(parse('varB = 4.242')),
			"Assign(Identifier('varb'), Constant(4.242))")

	def test_assign_float_negative(self):
		self.assertEqual(repr(parse('varC = -4.3')),
			"Assign(Identifier('varc'), UnaryOp('-', Constant(4.3)))")

	def test_assign_complex(self):
		self.assertEqual(repr(parse('varA = 2*i + 3')),
			"Assign(Identifier('vara'), BinaryOp(BinaryOp(Constant(2), '*', Identifier('i')), '+', Constant(3)))")

	def test_assign_complex_negative(self):
		self.assertEqual(repr(parse('varB =  -4i - 4')),
			"Assign(Identifier('varb'), BinaryOp(UnaryOp('-', BinaryOp(Constant(4), '*', Identifier('i'))), '-', Constant(4)))")

	def test_assign_matrix(self):
		self.assertEqual(repr(parse('varC = [[2,3];[4,3]]')),
			"Assign(Identifier('varc'), MatDecl([[Constant(2), Constant(3)], [Constant(4), Constant(3)]]))")

	def test_assign_function(self):
		self.assertEqual(repr(parse('funA(x) = 2x + 1')),
			"Assign(FunCall(Identifier('funa'), [Identifier('x')]), BinaryOp(BinaryOp(Constant(2), '*', Identifier('x')), '+', Constant(1)))")

	def test_assign_function_multiple_args(self):
		self.assertEqual(repr(parse('funB(x, y) = x * y')),
			"Assign(FunCall(Identifier('funb'), [Identifier('x'), Identifier('y')]), BinaryOp(Identifier('x'), '*', Identifier('y')))")

	def test_assign_uppercase(self):
		self.assertEqual(repr(parse('VARC = 2')),
			"Assign(Identifier('varc'), Constant(2))")

	def test_compute(self):
		self.assertEqual(repr(parse('2 * 21 = ?')),
			"BinaryOp(Constant(2), '*', Constant(21))")

	def test_compute_function(self):
		self.assertEqual(repr(parse('funA(2) = ?')),
			"FunCall(Identifier('funa'), [Constant(2)])")

	def test_priority(self):
		self.assertEqual(repr(parse('1 * 2 + 3')),
			"BinaryOp(BinaryOp(Constant(1), '*', Constant(2)), '+', Constant(3))")
		self.assertEqual(repr(parse('1 + 2 * 3')),
			"BinaryOp(Constant(1), '+', BinaryOp(Constant(2), '*', Constant(3)))")
		self.assertEqual(repr(parse('(1 + 2) * 3')),
			"BinaryOp(BinaryOp(Constant(1), '+', Constant(2)), '*', Constant(3))")

	def test_compute_eof(self):
		with self.assertRaises(EOFError):
			parse('a + 2 =')

	def test_solve(self):
		self.assertEqual(repr(parse('funA(x) = y ?')),
			"Solve(Assign(FunCall(Identifier('funa'), [Identifier('x')]), Identifier('y')))")

	def test_command(self):
		self.assertEqual(repr(parse('% foo')), "Command(['foo'])")

	def test_command_args(self):
		self.assertEqual(repr(parse('% foo bar baz')), "Command(['foo', 'bar', 'baz'])")

	def test_invalid_variable(self):
		with self.assertRaises(SyntaxError):
			parse('_var = 2')

	def test_unexcepted_token(self):
		with self.assertRaises(SyntaxError):
			parse('2 + * 2')

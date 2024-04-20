import unittest
from src.ast import *
from src.dtype import Matrix

class TestAst(unittest.TestCase):
	"""This class contains tests for the AST."""

	def test_assign(self):
		self.assertEqual(repr(Assign(Identifier('x'), Constant(1))),
			"Assign(Identifier('x'), Constant(1))")
		self.assertEqual(repr(Assign(Identifier('abc'), Constant(1.5))),
			"Assign(Identifier('abc'), Constant(1.5))")
		self.assertEqual(
			repr(Assign(FunCall(Identifier('f'), [Identifier('x')]), Identifier('x'))),
			"Assign(FunCall(Identifier('f'), [Identifier('x')]), Identifier('x'))")

	def test_binaryop(self):
		self.assertEqual(repr(BinaryOp(Constant(1), '+', Constant(2))),
			"BinaryOp(Constant(1), '+', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '/', Constant(2))),
			"BinaryOp(Constant(1), '/', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '**', Constant(2))),
			"BinaryOp(Constant(1), '**', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '%', Constant(2))),
			"BinaryOp(Constant(1), '%', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '*', Constant(2))),
			"BinaryOp(Constant(1), '*', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '^', Constant(2))),
			"BinaryOp(Constant(1), '^', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '-', Constant(2))),
			"BinaryOp(Constant(1), '-', Constant(2))")

	def test_binop_evaluate(self):
		self.assertEqual(BinaryOp(None, '+', None).evaluate(5, 8), 13)
		self.assertEqual(BinaryOp(None, '/', None).evaluate(14, 2), 7)
		self.assertEqual(BinaryOp(None, '%', None).evaluate(14, 3), 2)
		self.assertEqual(BinaryOp(None, '*', None).evaluate(5, 8), 40)
		self.assertEqual(BinaryOp(None, '^', None).evaluate(5, 3), 125)
		self.assertEqual(BinaryOp(None, '-', None).evaluate(5, 8), -3)

	def test_binop_evaluate_matmul(self):
		m1 = Matrix([[1, 2], [3, 4]])
		m2 = Matrix([[5, 6], [7, 8]])
		self.assertEqual(BinaryOp(None, '**', None).evaluate(m1, m2), Matrix([[19, 22], [43, 50]]))

	def test_binop_evaluate_matmul_invalid(self):
		with self.assertRaises(TypeError):
			BinaryOp(None, '**', None).evaluate(1, 2)

	def test_binop_get_associativity(self):
		self.assertEqual(BinaryOp(None, '+', None).get_associativity(), 'left')
		self.assertEqual(BinaryOp(None, '*', None).get_associativity(), 'left')
		self.assertEqual(BinaryOp(None, '**', None).get_associativity(), 'left')

	def test_binop_precedence(self):
		self.assertTrue(BinaryOp(None, '+', None).get_precedence() < BinaryOp(None, '*', None).get_precedence())
		self.assertTrue(BinaryOp(None, '*', None).get_precedence() > BinaryOp(None, '**', None).get_precedence())
		self.assertTrue(BinaryOp(None, '**', None).get_precedence() > BinaryOp(None, '+', None).get_precedence())

	def test_command(self):
		self.assertEqual(repr(Command(['foo', 'bar'])),"Command(['foo', 'bar'])")

	def test_constant(self):
		self.assertEqual(repr(Constant(1)), "Constant(1)")
		self.assertEqual(repr(Constant(1.5)), "Constant(1.5)")

	def test_funcall(self):
		self.assertEqual(repr(FunCall(Identifier('f'), [Constant(1)])),
			"FunCall(Identifier('f'), [Constant(1)])")
		self.assertEqual(repr(FunCall(Identifier('f'), [Constant(1), Constant(2)])),
			"FunCall(Identifier('f'), [Constant(1), Constant(2)])")

	def test_identifier(self):
		self.assertEqual(repr(Identifier('x')), "Identifier('x')")
		self.assertEqual(repr(Identifier('abc')), "Identifier('abc')")

	def test_matdecl(self):
		self.assertEqual(repr(MatDecl([[Constant(1), Constant(2)]])),
			"MatDecl([[Constant(1), Constant(2)]])")
		self.assertEqual(repr(MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])),
			"MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])")

	def test_unaryop(self):
		self.assertEqual(repr(UnaryOp('-', Constant(1))), "UnaryOp('-', Constant(1))")
		self.assertEqual(repr(UnaryOp('-', Constant(1))), "UnaryOp('-', Constant(1))")
		self.assertEqual(repr(UnaryOp('+', Constant(1))), "UnaryOp('+', Constant(1))")
		self.assertEqual(repr(UnaryOp('+', Constant(1))), "UnaryOp('+', Constant(1))")

	def test_unaryop_evaluate(self):
		self.assertEqual(UnaryOp('-', None).evaluate(5), -5)
		self.assertEqual(UnaryOp('+', None).evaluate(5), 5)
		self.assertEqual(UnaryOp('-', None).evaluate(5.5), -5.5)
		self.assertEqual(UnaryOp('+', None).evaluate(5.5), 5.5)

	def test_unaryop_precedence(self):
		self.assertEqual(UnaryOp('-', None).get_precedence(), UnaryOp('+', None).get_precedence())

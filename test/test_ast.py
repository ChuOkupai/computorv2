import unittest
from src.ast import *

class TestAst(unittest.TestCase):
	"""This class contains tests for the AST."""

	def test_constant(self):
		self.assertEqual(str(Constant(1)), '1')
		self.assertEqual(str(Constant(1.5)), '1.5')

	def test_identifier(self):
		self.assertEqual(str(Identifier('x')), 'x')
		self.assertEqual(str(Identifier('abc')), 'abc')

	def test_vardecl(self):
		self.assertEqual(str(VarDecl(Identifier('x'), Constant(1))), 'x = 1')
		self.assertEqual(str(VarDecl(Identifier('abc'), Constant(1.5))), 'abc = 1.5')

	def test_fundecl(self):
		self.assertEqual(str(FunDecl(Identifier('f'), [Identifier('x')], Identifier('x'))), 'f(x) = x')
		self.assertEqual(str(FunDecl(Identifier('f'), [Identifier('x'), Identifier('y')], Identifier('x'))), 'f(x, y) = x')

	def test_funcall(self):
		self.assertEqual(str(FunCall(Identifier('f'), [Constant(1)])), 'f(1)')
		self.assertEqual(str(FunCall(Identifier('f'), [Constant(1), Constant(2)])), 'f(1, 2)')

	def test_binaryop(self):
		self.assertEqual(str(BinaryOp(Constant(1), BinaryOpType.Add, Constant(2))), '(1 + 2)')
		self.assertEqual(str(BinaryOp(Constant(1), BinaryOpType.Div, Constant(2))), '(1 / 2)')
		self.assertEqual(str(BinaryOp(Constant(1), BinaryOpType.Mod, Constant(2))), '(1 % 2)')
		self.assertEqual(str(BinaryOp(Constant(1), BinaryOpType.Mul, Constant(2))), '(1 * 2)')
		self.assertEqual(str(BinaryOp(Constant(1), BinaryOpType.Pow, Constant(2))), '(1 ^ 2)')
		self.assertEqual(str(BinaryOp(Constant(1), BinaryOpType.Sub, Constant(2))), '(1 - 2)')

	def test_unaryop(self):
		self.assertEqual(str(UnaryOp(UnaryOpType.Neg, Constant(1))), '(-1)')
		self.assertEqual(str(UnaryOp(UnaryOpType.Pos, Constant(1))), '(+1)')

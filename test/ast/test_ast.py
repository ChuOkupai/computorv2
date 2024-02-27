import unittest
from src.ast import *

class TestAst(unittest.TestCase):
	"""This class contains tests for the AST."""

	def test_constant(self):
		self.assertEqual(repr(Constant(1)), "Constant(1)")
		self.assertEqual(repr(Constant(1.5)), "Constant(1.5)")

	def test_identifier(self):
		self.assertEqual(repr(Identifier('x')), "Identifier('x')")
		self.assertEqual(repr(Identifier('abc')), "Identifier('abc')")

	def test_vardecl(self):
		self.assertEqual(repr(VarDecl(Identifier('x'), Constant(1))), "VarDecl(Identifier('x'), Constant(1))")
		self.assertEqual(repr(VarDecl(Identifier('abc'), Constant(1.5))), "VarDecl(Identifier('abc'), Constant(1.5))")

	def test_matdecl(self):
		self.assertEqual(repr(MatDecl([[Constant(1), Constant(2)]])), "MatDecl([[Constant(1), Constant(2)]])")
		self.assertEqual(repr(MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])), "MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])")

	def test_fundecl(self):
		self.assertEqual(repr(FunDecl(Identifier('f'), [Identifier('x')], Identifier('x'))), "FunDecl(Identifier('f'), [Identifier('x')], Identifier('x'))")
		self.assertEqual(repr(FunDecl(Identifier('f'), [Identifier('x'), Identifier('y')], Identifier('x'))), "FunDecl(Identifier('f'), [Identifier('x'), Identifier('y')], Identifier('x'))")

	def test_funcall(self):
		self.assertEqual(repr(FunCall(Identifier('f'), [Constant(1)])), "FunCall(Identifier('f'), [Constant(1)])")
		self.assertEqual(repr(FunCall(Identifier('f'), [Constant(1), Constant(2)])), "FunCall(Identifier('f'), [Constant(1), Constant(2)])")

	def test_binaryop(self):
		self.assertEqual(repr(BinaryOp(Constant(1), '+', Constant(2))), "BinaryOp(Constant(1), '+', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '/', Constant(2))), "BinaryOp(Constant(1), '/', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '**', Constant(2))), "BinaryOp(Constant(1), '**', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '%', Constant(2))), "BinaryOp(Constant(1), '%', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '*', Constant(2))), "BinaryOp(Constant(1), '*', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '^', Constant(2))), "BinaryOp(Constant(1), '^', Constant(2))")
		self.assertEqual(repr(BinaryOp(Constant(1), '-', Constant(2))), "BinaryOp(Constant(1), '-', Constant(2))")

	def test_unaryop(self):
		self.assertEqual(repr(UnaryOp('-', Constant(1))), "UnaryOp('-', Constant(1))")
		self.assertEqual(repr(UnaryOp('-', Constant(1))), "UnaryOp('-', Constant(1))")
		self.assertEqual(repr(UnaryOp('+', Constant(1))), "UnaryOp('+', Constant(1))")
		self.assertEqual(repr(UnaryOp('+', Constant(1))), "UnaryOp('+', Constant(1))")

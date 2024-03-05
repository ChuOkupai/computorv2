import unittest
from src.ast import *

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

	def test_constant(self):
		self.assertEqual(repr(Constant(1)), "Constant(1)")
		self.assertEqual(repr(Constant(1.5)), "Constant(1.5)")

	def test_identifier(self):
		self.assertEqual(repr(Identifier('x')), "Identifier('x')")
		self.assertEqual(repr(Identifier('abc')), "Identifier('abc')")

	def test_matdecl(self):
		self.assertEqual(repr(MatDecl([[Constant(1), Constant(2)]])),
			"MatDecl([[Constant(1), Constant(2)]])")
		self.assertEqual(repr(MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])),
			"MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])")

	def test_funcall(self):
		self.assertEqual(repr(FunCall(Identifier('f'), [Constant(1)])),
			"FunCall(Identifier('f'), [Constant(1)])")
		self.assertEqual(repr(FunCall(Identifier('f'), [Constant(1), Constant(2)])),
			"FunCall(Identifier('f'), [Constant(1), Constant(2)])")

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

	def test_unaryop(self):
		self.assertEqual(repr(UnaryOp('-', Constant(1))), "UnaryOp('-', Constant(1))")
		self.assertEqual(repr(UnaryOp('-', Constant(1))), "UnaryOp('-', Constant(1))")
		self.assertEqual(repr(UnaryOp('+', Constant(1))), "UnaryOp('+', Constant(1))")
		self.assertEqual(repr(UnaryOp('+', Constant(1))), "UnaryOp('+', Constant(1))")

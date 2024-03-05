import unittest
from src.ast import *
from src.ast import RenderVisitor as Rv

class TestAst(unittest.TestCase):
	"""This class contains tests for the RenderVisitor class."""

	def test_assign(self):
		self.assertEqual(Rv().visit(Assign(Identifier('foo'), Constant(1))),
			'foo = 1')
		self.assertEqual(Rv().visit(Assign(Identifier('bar'), Constant(1.5))),
			'bar = 1.5')
		self.assertEqual(Rv().visit(Assign(Identifier('baz'), Identifier('foo'))),
			'baz = foo')

	def test_binaryop(self):
		self.assertEqual(Rv().visit(BinaryOp(Constant(1), '+', Constant(2))), '1 + 2')
		self.assertEqual(Rv().visit(BinaryOp(Constant(1), '/', Constant(2))), '1 / 2')
		self.assertEqual(Rv().visit(BinaryOp(Constant(1), '**', Constant(2))), '1 ** 2')
		self.assertEqual(Rv().visit(BinaryOp(Constant(1), '%', Constant(2))), '1 % 2')
		self.assertEqual(Rv().visit(BinaryOp(Constant(1), '*', Constant(2))), '1 * 2')
		self.assertEqual(Rv().visit(BinaryOp(Constant(1), '^', Constant(2))), '1 ^ 2')
		self.assertEqual(Rv().visit(BinaryOp(Constant(1), '-', Constant(2))), '1 - 2')

	def test_constant(self):
		self.assertEqual(Rv().visit(Constant(1)), '1')
		self.assertEqual(Rv().visit(Constant(1.5)), '1.5')

	def test_funcall(self):
		self.assertEqual(Rv().visit(FunCall(Identifier('foo'), [Constant(1)])),
			'foo(1)')
		self.assertEqual(Rv().visit(FunCall(Identifier('bar'), [Constant(1), Constant(2)])),
			'bar(1, 2)')

	def test_identifier(self):
		self.assertEqual(Rv().visit(Identifier('foo')), 'foo')
		self.assertEqual(Rv().visit(Identifier('bar')), 'bar')

	def test_matdecl(self):
		self.assertEqual(Rv().visit(MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])),
			'[[1, 2]; [3, 4]]')

	def test_solve(self):
		self.assertEqual(Rv().visit(Solve(Assign(Identifier('x'), Constant(1)))), 'x = 1 ?')

	def test_unaryop(self):
		self.assertEqual(Rv().visit(UnaryOp('-', Constant(1))), '-1')
		self.assertEqual(Rv().visit(UnaryOp('+', Constant(1))), '1')

	def test_priority(self):
		self.assertEqual(Rv().visit(BinaryOp(Constant(1), '*', BinaryOp(Constant(2), '+', Constant(3)))),
			'1 * (2 + 3)')
		self.assertEqual(Rv().visit(BinaryOp(BinaryOp(Constant(1), '+', Constant(2)), '*', Constant(3))),
			'(1 + 2) * 3')

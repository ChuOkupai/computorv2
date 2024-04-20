import unittest
from src.ast import *
from src.ast import RenderVisitor as R

class TestRenderVisitor(unittest.TestCase):
	"""This class contains tests for the render visitor."""

	def test_assign(self):
		self.assertEqual(R().visit(Assign(Identifier('foo'), Constant(1))),
			'foo = 1')
		self.assertEqual(R().visit(Assign(Identifier('bar'), Constant(1.5))),
			'bar = 1.5')
		self.assertEqual(R().visit(Assign(Identifier('baz'), Identifier('foo'))),
			'baz = foo')

	def test_binaryop(self):
		self.assertEqual(R().visit(BinaryOp(Constant(1), '+', Constant(2))), '1 + 2')
		self.assertEqual(R().visit(BinaryOp(Constant(1), '/', Constant(2))), '1 / 2')
		self.assertEqual(R().visit(BinaryOp(Constant(1), '**', Constant(2))), '1 ** 2')
		self.assertEqual(R().visit(BinaryOp(Constant(1), '%', Constant(2))), '1 % 2')
		self.assertEqual(R().visit(BinaryOp(Constant(1), '*', Constant(2))), '1 * 2')
		self.assertEqual(R().visit(BinaryOp(Constant(1), '^', Constant(2))), '1 ^ 2')
		self.assertEqual(R().visit(BinaryOp(Constant(1), '-', Constant(2))), '1 - 2')

	def test_command(self):
		self.assertEqual(R().visit(Command(['foo', 'bar'])), '% foo bar')

	def test_constant(self):
		self.assertEqual(R().visit(Constant(1)), '1')
		self.assertEqual(R().visit(Constant(1.5)), '1.5')

	def test_funcall(self):
		self.assertEqual(R().visit(FunCall(Identifier('foo'), [Constant(1)])),
			'foo(1)')
		self.assertEqual(R().visit(FunCall(Identifier('bar'), [Constant(1), Constant(2)])),
			'bar(1, 2)')

	def test_identifier(self):
		self.assertEqual(R().visit(Identifier('foo')), 'foo')
		self.assertEqual(R().visit(Identifier('bar')), 'bar')

	def test_matdecl(self):
		self.assertEqual(R().visit(MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])),
			'[[1, 2]; [3, 4]]')

	def test_solve(self):
		self.assertEqual(R().visit(Solve(Assign(Identifier('x'), Constant(1)))), 'x = 1 ?')

	def test_unaryop(self):
		self.assertEqual(R().visit(UnaryOp('-', Constant(1))), '-1')
		self.assertEqual(R().visit(UnaryOp('+', Constant(1))), '1')

	def test_priority(self):
		self.assertEqual(R().visit(BinaryOp(Constant(1), '*', BinaryOp(Constant(2), '+', Constant(3)))),
			'1 * (2 + 3)')
		self.assertEqual(R().visit(BinaryOp(BinaryOp(Constant(1), '+', Constant(2)), '*', Constant(3))),
			'(1 + 2) * 3')

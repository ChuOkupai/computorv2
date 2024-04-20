import unittest
from src.ast import Assign, BinaryOp, Command, Constant, FunCall, Identifier, MatDecl, Solve, \
	UnaryOp
from src.dtype import Complex, Polynomial
from src.interpreter import InvalidPolynomialError, PolynomialVisitor

class TestPolynomialVisitor(unittest.TestCase):
	"""This class tests the PolynomialVisitor class."""

	def _test_ast(self, left_polynomial, right_polynomial):
		ast = Solve(Assign(left_polynomial, right_polynomial))
		pv = PolynomialVisitor()
		return pv.visit(ast)

	def test_command(self):
		with self.assertRaises(InvalidPolynomialError):
			self._test_ast(Command(['foo', 'bar']), Constant(0))

	def test_const(self):
		p = self._test_ast(Constant(42), Constant(0))
		self.assertEqual(p, Polynomial({0: 42}))

	def test_var(self):
		p = self._test_ast(Identifier('x'), Constant(0))
		self.assertEqual(p, Polynomial({1: 1}))

	def test_var_power(self):
		p = self._test_ast(BinaryOp(Identifier('x'), '^', Constant(2)), Constant(0))
		self.assertEqual(p, Polynomial({2: 1}))

	def test_const_var(self):
		p = self._test_ast(BinaryOp(Constant(2), '*', Identifier('x')), Constant(0))
		self.assertEqual(p, Polynomial({1: 2}))

	def test_term(self):
		p = self._test_ast(BinaryOp(Constant(2), '*', BinaryOp(Identifier('x'), '^',
			Constant(2))), Constant(0))
		self.assertEqual(p, Polynomial({2: 2}))

	def test_add(self):
		p = self._test_ast(BinaryOp(Identifier('x'), '+', Identifier('x')), Constant(0))
		self.assertEqual(p, Polynomial({1: 2}))

	def test_sub(self):
		p = self._test_ast(BinaryOp(Identifier('x'), '-', Identifier('x')), Constant(0))
		self.assertEqual(p, Polynomial())

	def test_uadd(self):
		p = self._test_ast(UnaryOp('+', Identifier('x')), Constant(0))
		self.assertEqual(p, Polynomial({1: 1}))

	def test_usub(self):
		p = self._test_ast(UnaryOp('-', Identifier('x')), Constant(0))
		self.assertEqual(p, Polynomial({1: -1}))

	def test_invalid_const(self):
		with self.assertRaises(InvalidPolynomialError):
			self._test_ast(Constant(Complex(1, 1)), Constant(0))

	def test_invalid_pow(self):
		with self.assertRaises(InvalidPolynomialError):
			self._test_ast(BinaryOp(Identifier('x'), '^', Constant(0.5)), Constant(0))

	def test_invalid_op(self):
		with self.assertRaises(InvalidPolynomialError):
			self._test_ast(BinaryOp(Identifier('x'), '/', Identifier('x')), Constant(0))

	def test_funcall(self):
		with self.assertRaises(InvalidPolynomialError):
			self._test_ast(FunCall(Identifier('f'), [Identifier('x')]), Constant(0))

	def test_matdecl(self):
		with self.assertRaises(InvalidPolynomialError):
			self._test_ast(MatDecl([[Constant(1)]]), Constant(0))

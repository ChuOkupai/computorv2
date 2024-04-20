import unittest
from src.ast import Assign, BinaryOp, Command, Constant, FunCall, Identifier, MatDecl, Solve, \
	UnaryOp
from src.dtype import Matrix
from src.interpreter import Context, EvaluatorVisitor, FunctionStorage, InterpreterErrorGroup

class TestEvaluatorVisitor(unittest.TestCase):
	"""This class tests the EvaluatiorVisitor class."""

	def _assert_constant_eq(self, node, value):
		self.assertIsInstance(node, Constant)
		self.assertEqual(node.value, value)

	def _assert_var_exist(self, name, value):
		var = self.ctx.get_variable(name)
		self._assert_constant_eq(var, value)

	def setUp(self):
		self.ctx = Context()
		self.ctx.set_function('f',
			FunctionStorage([Identifier('x')], BinaryOp(Identifier('x'), '*', Constant(2))))
		self.ctx.set_variable('a', Constant(1))
		self.ctx.set_variable('b', Constant(2))
		self.ev = EvaluatorVisitor(self.ctx)

	def test_assign_constant(self):
		ast = Assign(Identifier('x'), Constant(1))
		self.ev.visit(ast)
		self._assert_var_exist('x', 1)

	def test_assign_function(self):
		ast = Assign(FunCall(Identifier('add'), [Identifier('x'), Identifier('y')]),
			BinaryOp(Identifier('x'), '+', Identifier('y')))
		self.ev.visit(ast)
		add = self.ctx.get_function('add')
		self.assertIsInstance(add, FunctionStorage)
		self.assertEqual(repr(add.args), "[Identifier('x'), Identifier('y')]")
		self.assertEqual(repr(add.body), "BinaryOp(Identifier('x'), '+', Identifier('y'))")

	def test_assign_function_calling_builtin_function(self):
		ast = Assign(FunCall(Identifier('foo'), [Identifier('x')]),
			UnaryOp('-', FunCall(Identifier('sin'), [Identifier('x')])))
		expected = repr(ast.value)
		self.ev.visit(ast)
		z = self.ctx.get_function('foo')
		self.assertIsInstance(z, FunctionStorage)
		self.assertEqual(repr(z.args), "[Identifier('x')]")
		self.assertEqual(repr(z.body), expected)

	def test_assign_function_calling_user_defined_function(self):
		ast = Assign(FunCall(Identifier('foo'), [Identifier('x')]),
			FunCall(Identifier('f'), [Identifier('x')]))
		expected = repr(ast.value)
		self.ev.visit(ast)
		z = self.ctx.get_function('foo')
		self.assertIsInstance(z, FunctionStorage)
		self.assertEqual(repr(z.args), "[Identifier('x')]")
		self.assertEqual(repr(z.body), expected)

	def test_assign_function_mask_variable(self):
		ast = Assign(FunCall(Identifier('f'), [Identifier('a')]), Identifier('a'))
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res), "Identifier('a')")

	def test_binaryop(self):
		ast = BinaryOp(Constant(6), '*', Constant(7))
		self.ev.visit(ast)
		self._assert_constant_eq(self.ev.res, 42)

	def test_command(self):
		ast = Command(['clear'])
		self.ev.visit(ast)

	def test_constant(self):
		ast = Constant(9000)
		self.ev.visit(ast)
		self._assert_constant_eq(self.ev.res, 9000)

	def test_funcall_builtin(self):
		ast = FunCall(Identifier('cos'), [Constant(0)])
		self.ev.visit(ast)
		self._assert_constant_eq(self.ev.res, 1.0)

	def test_funcall_nested(self):
		ast = FunCall(Identifier('f'), [FunCall(Identifier('f'), [Constant(10)])])
		self.ev.visit(ast)
		self._assert_constant_eq(self.ev.res, 40)

	def test_funcall_nested_with_undefined_args(self):
		ast = FunCall(Identifier('f'), [FunCall(Identifier('f'), [Identifier('x')])])
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res),
			"BinaryOp(BinaryOp(Identifier('x'), '*', Constant(2)), '*', Constant(2))")

	def test_funcall_undefined(self):
		ast = FunCall(Identifier('foo'), [Constant(1)])
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res), "FunCall(Identifier('foo'), [Constant(1)])")

	def test_funcall_user_defined(self):
		ast = FunCall(Identifier('f'), [Constant(21)])
		self.ev.visit(ast)
		self._assert_constant_eq(self.ev.res, 42)

	def test_funcall_user_defined_with_undefined_args(self):
		ast = FunCall(Identifier('f'), [Identifier('y')])
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res), "BinaryOp(Identifier('y'), '*', Constant(2))")

	def test_identifier_declared(self):
		ast = Identifier('a')
		self.ev.visit(ast)
		self._assert_constant_eq(self.ev.res, 1)

	def test_identifier_undeclared(self):
		ast = Identifier('x')
		self.ev.visit(ast)
		r = self.ev.res
		self.assertIsInstance(r, Identifier)
		self.assertEqual(r.value, 'x')

	def test_mat_decl(self):
		ast = MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])
		self.ev.visit(ast)
		self._assert_constant_eq(self.ev.res, Matrix([[1, 2], [3, 4]]))

	def test_mat_decl_non_const(self):
		ast = MatDecl([[Constant(1), Identifier('x')], [Constant(3), Constant(4)]])
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res), "MatDecl([[Constant(1), Identifier('x')], [Constant(3), Constant(4)]])")

	def test_mat_decl_implicit_conversion(self):
		ast = MatDecl([[Constant(1), Identifier('i'), Constant(3)]])
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res),
			"Constant(Matrix([[Complex(1), Complex(0, 1), Complex(3)]]))")

	def test_reassign_function_with_different_args(self):
		ast = Assign(FunCall(Identifier('g'), [Identifier('x')]),
			FunCall(Identifier('f'), [Identifier('x')]))
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res), "FunCall(Identifier('f'), [Identifier('x')])")
		ast = Assign(FunCall(Identifier('f'), [Identifier('x'), Identifier('y')]),
			BinaryOp(Identifier('x'), '+', Identifier('y')))
		with self.assertRaises(InterpreterErrorGroup):
			self.ev.visit(ast)

	def test_solve(self):
		ast = Solve(Assign(BinaryOp(Identifier('x'), '+', Constant(1)), Constant(8)))
		self.assertEqual(repr(self.ev.visit(ast)), "Constant(7)")

	def test_solve_2(self):
		ast = Solve(Assign(BinaryOp(BinaryOp(BinaryOp(Identifier('x'), '^', Constant(2)), '+',
		BinaryOp(Constant(3), '*', Identifier('x'))), '-', Constant(4)), Constant(0)))
		self.assertEqual(repr(self.ev.visit(ast)), "Constant(Matrix([[-4, 1]]))")

	def test_unaryop_constant(self):
		ast = UnaryOp('-', Constant(1))
		self.ev.visit(ast)
		self._assert_constant_eq(self.ev.res, -1)

	def test_unaryop_multiple(self):
		ast = UnaryOp('-', UnaryOp('+', UnaryOp('-', Constant(1))))
		self.ev.visit(ast)
		self._assert_constant_eq(self.ev.res, 1)

	def test_unaryop_simplify_positive(self):
		ast = UnaryOp('+', Identifier('z'))
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res), "Identifier('z')")

	def test_unaryop_simplify_double_negative(self):
		ast = UnaryOp('-', UnaryOp('-', Identifier('z')))
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res), "Identifier('z')")

	def test_unaryop_undefined(self):
		ast = UnaryOp('-', Identifier('x'))
		self.ev.visit(ast)
		self.assertEqual(repr(self.ev.res), "UnaryOp('-', Identifier('x'))")

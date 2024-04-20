import unittest
from src.ast import Assign, BinaryOp, Command, Constant, FunCall, Identifier, MatDecl, Solve, \
	UnaryOp
from src.interpreter.errors import *
from src.interpreter import Context, FunctionStorage, DependenciesVisitor

class TestDependenciesVisitor(unittest.TestCase):
	"""This class tests the DependenciesVisitor class."""

	def setUp(self):
		self.ctx = Context()
		self.ctx.set_function('f',
			FunctionStorage([Identifier('x')], Identifier('x')))
		self.ctx.set_function('g',
			FunctionStorage([Identifier('y')], Identifier('y')))
		self.dv = DependenciesVisitor(self.ctx)

	def test_get_undefined_variables(self):
		self.dv.visit(BinaryOp(Identifier('x'), '+', Identifier('y')))
		self.assertEqual(self.dv.get_undefined_variables(), {'x', 'y'})

	def test_get_undefined_variables_with_constants(self):
		self.dv.visit(BinaryOp(Identifier('x'), '+', Identifier('pi')))
		self.assertEqual(self.dv.get_undefined_variables(), {'x'})

	def test_get_user_defined_functions(self):
		self.dv.visit(FunCall(Identifier('f'), [Identifier('x')]))
		self.dv.visit(FunCall(Identifier('g'), [Identifier('y')]))
		self.dv.visit(FunCall(Identifier('sin'), [Constant(1)]))
		self.assertEqual(self.dv.get_user_defined_functions(), {'f', 'g'})

	def test_matdecl(self):
		expr = MatDecl([[Constant(1), Constant(2)], [Constant(3), Constant(4)]])
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, set())
		self.assertEqual(self.dv.visited_variables, set())

	def test_matdecl_with_functions(self):
		expr = MatDecl([[FunCall(Identifier('f'), [Constant(1)])]])
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, {'f'})
		self.assertEqual(self.dv.visited_variables, set())

	def test_matdecl_with_variables(self):
		expr = MatDecl([[Identifier('x'), Identifier('y')]])
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, set())
		self.assertEqual(self.dv.visited_variables, {'x', 'y'})

	def test_multiple_functions(self):
		expr = FunCall(Identifier('f'), [FunCall(Identifier('g'), [Constant(1)])])
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, {'f', 'g'})
		self.assertEqual(self.dv.visited_variables, set())

	def test_multiple_variables(self):
		expr = BinaryOp(Identifier('x'), '+', Identifier('y'))
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, set())
		self.assertEqual(self.dv.visited_variables, {'x', 'y'})

	def test_nested_variables(self):
		expr = BinaryOp(Identifier('x'), '+', BinaryOp(Identifier('y'), '+', Identifier('z')))
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, set())
		self.assertEqual(self.dv.visited_variables, {'x', 'y', 'z'})

	def test_no_dependencies(self):
		expr = BinaryOp(Constant(1), '+', Constant(2))
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, set())
		self.assertEqual(self.dv.visited_variables, set())

	def test_single_assignment(self):
		expr = Assign(Identifier('x'), Constant(1))
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, set())
		self.assertEqual(self.dv.visited_variables, {'x'})

	def test_single_builtin_function(self):
		expr = FunCall(Identifier('sin'), [Constant(1)])
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, {'sin'})
		self.assertEqual(self.dv.visited_variables, set())

	def test_single_user_defined_function(self):
		expr = FunCall(Identifier('f'), [Constant(1)])
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, {'f'})
		self.assertEqual(self.dv.visited_variables, set())

	def test_single_variable(self):
		expr = Identifier('x')
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, set())
		self.assertEqual(self.dv.visited_variables, {'x'})

	def test_solve(self):
		expr = Solve(Assign(Identifier('x'), Identifier('y')))
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, set())
		self.assertEqual(self.dv.visited_variables, {'x', 'y'})

	def test_unaryop(self):
		expr = UnaryOp('-', FunCall(Identifier('f'), [Identifier('x')]))
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, {'f'})
		self.assertEqual(self.dv.visited_variables, {'x'})

	def test_command(self):
		expr = Command(['foo', 'bar'])
		self.dv.visit(expr)
		self.assertEqual(self.dv.visited_functions, set())
		self.assertEqual(self.dv.visited_variables, set())

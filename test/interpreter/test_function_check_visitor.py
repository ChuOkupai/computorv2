import unittest
from src.ast import Assign, BinaryOp, Constant, FunCall, Identifier, MatDecl, Solve, UnaryOp
from src.interpreter.exceptions import *
from src.interpreter import Context
from src.interpreter import FunctionStorage as Fs
from src.interpreter import FunctionCheckVisitor as Fc

class TestFunctionCheckVisitor(unittest.TestCase):
	'''This class checks if all exceptions are raised correctly.'''

	def setUp(self):
		self.ctx = Context()
		self.ast = Assign(None, None)

	def test_cyclic_dependency_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = Identifier('x')
		Fc(self.ctx).visit(self.ast)
		self.ast.value = FunCall(Identifier('f'), [Identifier('x')])
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], CyclicDependencyError))

	def test_invalid_arguments_length_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('cos'), [Identifier('x'), Identifier('x')])
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], InvalidArgumentsLengthError))

	def test_multiple_declaration_error(self):
		self.ast.target = FunCall(Identifier('f'),
			[Identifier('x'), Identifier('x'), Identifier('y'), Identifier('x')])
		self.ast.value = BinaryOp(Identifier('x'), '+', Identifier('y'))
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], MultipleDeclarationError))

	def test_require_identifier_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x'), Constant(1)])
		self.ast.value = Identifier('x')
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], RequireIdentifierError))

	def test_unused_parameter_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x'), Identifier('y')])
		self.ast.value = Identifier('x')
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], UnusedParameterError))

	def test_built_in_constant_error(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x'), Identifier('pi')])
		self.ast.value = BinaryOp(Identifier('x'), '*', Identifier('pi'))
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], BuiltInConstantError))

	def test_call_undefined_function(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('g'), [Identifier('x')])
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], UndefinedSymbolError))

	def test_call_undefined_variable(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = BinaryOp(Identifier('x'), '+', Identifier('y'))
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], UndefinedSymbolError))

	def test_call_invalid_arguments_length(self):
		self.ctx.set_function('f', Fs([Identifier('x')], Identifier('x')))
		self.ast.target = FunCall(Identifier('g'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('f'), [Identifier('x'), Identifier('x')])
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], InvalidArgumentsLengthError))

	def test_call_invalid_arguments_length_2(self):
		self.ctx.set_function('f', Fs([Identifier('x'), Identifier('y')], Identifier('x')))
		self.ast.target = FunCall(Identifier('g'), [Identifier('x')])
		self.ast.value = FunCall(Identifier('f'), [Identifier('x')])
		with self.assertRaises(InterpreterErrorGroup) as el:
			Fc(self.ctx).visit(self.ast)
		el = el.exception
		self.assertEqual(len(el.errors), 1)
		self.assertTrue(isinstance(el.errors[0], InvalidArgumentsLengthError))

	def test_solve(self):
		with self.assertRaises(NotImplementedError):
			Fc(self.ctx).visit(Solve(None))

	def test_matdecl(self):
		self.ast.target = FunCall(Identifier('f'), [Identifier('x')])
		self.ast.value = MatDecl([[Constant(1), Identifier('x')]])
		Fc(self.ctx).visit(self.ast)

	def test_unaryop(self):
		Fc(self.ctx).visit(UnaryOp('-', Constant(1)))

import unittest
from src.dtype import Complex, Polynomial
from src.interpreter import ConstantEquationSolver, EquationSolverFactory, \
	InvalidPolynomialDegreeError, LinearEquationSolver, QuadraticEquationSolver

class TestEquationSolvers(unittest.TestCase):
	"""This class tests the EquationSolverFactory class and its subclasses."""

	def test_equation_solver_factory_0(self):
		solver = EquationSolverFactory.create(Polynomial({0: 0}))
		self.assertIsInstance(solver, ConstantEquationSolver)

	def test_equation_solver_factory_1(self):
		solver = EquationSolverFactory.create(Polynomial({0: 0, 1: 1}))
		self.assertIsInstance(solver, LinearEquationSolver)

	def test_equation_solver_factory_2(self):
		solver = EquationSolverFactory.create(Polynomial({0: 0, 1: 1, 2: 1}))
		self.assertIsInstance(solver, QuadraticEquationSolver)

	def test_equation_solver_factory_negative_degree(self):
		with self.assertRaises(InvalidPolynomialDegreeError):
			EquationSolverFactory.create(Polynomial({-2: 1}))

	def test_equation_solver_factory_too_high_degree(self):
		with self.assertRaises(InvalidPolynomialDegreeError):
			EquationSolverFactory.create(Polynomial({0: 0, 1: 1, 2: 1, 3: 1}))

	def test_constant_equation_solver_any(self):
		p = Polynomial({0: 0})
		solver = ConstantEquationSolver()
		self.assertEqual(solver.solve(p), float('inf'))

	def test_constant_equation_solver_impossible(self):
		p = Polynomial({0: 1})
		solver = ConstantEquationSolver()
		self.assertTrue(float('nan'), solver.solve(p))

	def test_linear_equation_solver(self):
		p = Polynomial({0: 1, 1: 2})
		solver = LinearEquationSolver()
		self.assertEqual(solver.solve(p), -0.5)

	def test_quadratic_equation_solver_zero_discriminant(self):
		p = Polynomial({0: 1, 1: 2, 2: 1})
		solver = QuadraticEquationSolver()
		self.assertEqual(solver.solve(p), -1)

	def test_quadratic_equation_solver_positive_discriminant(self):
		p = Polynomial({0: 6, 1: 5, 2: 1})
		solver = QuadraticEquationSolver()
		self.assertEqual(solver.solve(p), [-3.0, -2.0])

	def test_quadratic_equation_solver_negative_discriminant(self):
		p = Polynomial({0: 5, 1: 4, 2: 1})
		solver = QuadraticEquationSolver()
		self.assertEqual(solver.solve(p), [Complex(-2, -1), Complex(-2, 1)])

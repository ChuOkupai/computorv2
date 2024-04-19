import math
from abc import ABC, abstractmethod
from src.dtype import Complex, Polynomial
from src.interpreter import InvalidPolynomialDegreeError

class EquationSolver(ABC):
	"""Class for solving equations."""

	def _get_n_coeffs(self, p, n):
		"""Get n coefficients from the polynomial."""
		return [p.get_coefficient(i) for i in reversed(range(n))]

	@abstractmethod
	def solve(self, p: Polynomial):
		"""Solve the equation."""
		pass

class ConstantEquationSolver(EquationSolver):
	"""Class for solving constant equations."""

	def solve(self, p):
		return float('inf' if self._get_n_coeffs(p, 1)[0] == 0 else 'nan')

class LinearEquationSolver(EquationSolver):
	"""Class for solving linear equations."""

	def solve(self, p):
		a, b = self._get_n_coeffs(p, 2)
		return -b / a

class QuadraticEquationSolver(EquationSolver):
	"""Class for solving quadratic equations."""

	def solve(self, p):
		a, b, c = self._get_n_coeffs(p, 3)
		d = b * b - 4 * a * c
		if d == 0:
			return -b / (2 * a)
		sdelta = math.sqrt(abs(d))
		a *= 2
		if d > 0:
			return [(-b + s * sdelta) / a for s in (-1, 1)]
		num, den = -b / a, sdelta / a
		return [Complex(num, s * den) for s in (-1, 1)]

class EquationSolverFactory():
	"""Factory for creating equation solvers."""

	solvers = [
		ConstantEquationSolver,
		LinearEquationSolver,
		QuadraticEquationSolver
	]

	@staticmethod
	def create(p: Polynomial):
		"""Create a solver for the given polynomial."""
		deg = p.get_degree()
		if deg >= 0 and deg < len(EquationSolverFactory.solvers):
			return EquationSolverFactory.solvers[p.get_degree()]()
		raise InvalidPolynomialDegreeError(deg)

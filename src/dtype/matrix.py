import math
from copy import deepcopy
from src.dtype import Complex, InvalidShapeError, NotSquareError

def is_close(x, y, abs_tol=1e-9):
	if isinstance(x, Complex):
		return abs(x - y) < abs_tol
	return math.isclose(x, y, abs_tol=abs_tol)

class Matrix:
	pass

class Matrix:
	"""This class represents a matrix."""

	@staticmethod
	def identity(n: int, dtype=float):
		return Matrix([[dtype(i == j) for j in range(n)] for i in range(n)])

	def __init__(self, values: list):
		if any(len(x) != len(values[0]) for x in values):
			raise InvalidShapeError
		if any(any(not isinstance(y, type(values[0][0])) for y in x) for x in values):
			raise SyntaxError("all elements in the matrix must be of the same type.")
		self.shape = (len(values), len(values[0]))
		self.values = values

	def _assert_same_shape(self, other):
		if self.shape != other.shape:
			raise InvalidShapeError

	def _assert_square(self):
		if not self.is_square():
			raise NotSquareError

	def _do_op_matrix(self, other, op):
		self._assert_same_shape(other)
		return Matrix([[op(x, y) for x, y in zip(r1, r2)] for r1, r2 in zip(self.values, other.values)])

	def _rref(self):
		m = self.values
		for i in range(self.rows()):
			for j in range(self.cols()):
				if ((isinstance(m[i][j], (float, int)) and m[i][j] != 0)
					or (isinstance(m[i][j], Complex) and m[i][j].r != 0)):
					m[i] = [x / m[i][j] for x in m[i]]
					for k in range(self.rows()):
						if k != i:
							m[k] = [x - y * m[k][j] for x, y in zip(m[k], m[i])]
					break

	def cols(self):
		return self.shape[1]

	def rows(self):
		return self.shape[0]

	def is_close(self, other: Matrix, delta=1e-9):
		if self.shape != other.shape:
			return False
		return all(all(is_close(x, y, abs_tol=delta) for x, y in zip(r1, r2)) for r1, r2 in zip(self.values, other.values))

	def is_square(self):
		return self.cols() == self.rows()

	def transpose(self):
		return Matrix([[self.values[j][i] for j in range(self.rows())] for i in range(self.cols())])

	def inverse(self):
		self._assert_square()
		a2 = deepcopy(self)
		dtype = type(self.values[0][0]) if self.cols() > 0 else float
		id = Matrix.identity(self.rows(), dtype=dtype)
		for i in range(a2.rows()):
			a2.values[i] += id.values[i]
		a2.shape = (a2.rows(), 2 * a2.cols())
		a2._rref()
		for i in range(a2.rows()):
			a2.values[i] = a2.values[i][a2.cols() // 2:]
		a2.shape = (a2.rows(), a2.cols() // 2)
		id2 = self * a2
		if id2.is_close(id):
			return a2
		raise ValueError("Matrix is not invertible")

	def __add__(self, other):
		if isinstance(other, Matrix):
			return self._do_op_matrix(other, lambda x, y: x + y)
		raise NotImplementedError

	def __mul__(self, other):
		if isinstance(other, (Complex, float, int)):
			return Matrix([[x * other for x in r] for r in self.values])
		if isinstance(other, Matrix):
			if self.cols() != other.rows():
				raise InvalidShapeError("Number of columns in first matrix must equal number of rows in second matrix")
			return Matrix([[sum(x * y for x, y in zip(r1, r2)) for r2 in zip(*other.values)] for r1 in self.values])
		raise NotImplementedError

	def __radd__(self, other):
		return self + other

	def __rmul__(self, other):
		return self * other

	def __sub__(self, other):
		if isinstance(other, Matrix):
			return self._do_op_matrix(other, lambda x, y: x - y)
		raise NotImplementedError

	def __str__(self):
		return str('\n'.join(str(r) for r in self.values))

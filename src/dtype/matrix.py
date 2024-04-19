from copy import deepcopy
from src.dtype import Complex, is_close, is_literal

class Matrix:
	pass

class Matrix:
	"""This class represents a matrix."""

	class InvalidShapeError(ValueError):
		def __init__(self):
			super().__init__('invalid matrix shape.')

	class NotSquareError(ValueError):
		def __init__(self):
			super().__init__('matrix is not square.')

	@staticmethod
	def identity(n: int, dtype=float):
		return Matrix([[dtype(i == j) for j in range(n)] for i in range(n)])

	@staticmethod
	def ones(n: int, m: int, dtype=float):
		return Matrix([[dtype(1) for _ in range(m)] for _ in range(n)])

	@staticmethod
	def zeros(n: int, m: int, dtype=float):
		return Matrix([[dtype(0) for _ in range(m)] for _ in range(n)])

	def __init__(self, values: list):
		if any(len(x) != len(values[0]) for x in values):
			raise self.InvalidShapeError
		if not is_literal(values[0][0]):
			raise ValueError('all elements in the matrix must be literals.')
		if any(any(not isinstance(y, type(values[0][0])) for y in x) for x in values):
			if any(any(isinstance(y, Complex) for y in x) for x in values):
				values = [[x if isinstance(x, Complex) else Complex(x) for x in r] for r in
					values]
			else:
				raise ValueError('all elements in the matrix must be of the same type.')
		self.shape = (len(values), len(values[0]))
		self.values = values

	def _do_op(self, m, op):
		if isinstance(m, Matrix):
			if self.shape != m.shape:
				raise self.InvalidShapeError
			return Matrix([[op(x, y) for x, y in zip(r1, r2)] for r1, r2 in zip(self.values, m.values)])
		return Matrix([[op(x, m) for x in r] for r in self.values])

	def _rref(self):
		m = self.values
		for i in range(self.rows()):
			for j in range(self.cols()):
				if m[i][j] != 0:
					m[i] = [x / m[i][j] for x in m[i]]
					for k in range(self.rows()):
						if k != i:
							m[k] = [x - y * m[k][j] for x, y in zip(m[k], m[i])]
					break

	def cols(self):
		return self.shape[1]

	def rows(self):
		return self.shape[0]

	def inverse(self):
		if self.cols() != self.rows():
			raise self.NotSquareError
		a2 = deepcopy(self)
		id = Matrix.identity(self.rows(), dtype=type(self.values[0][0]))
		for i in range(a2.rows()):
			a2.values[i] += id.values[i]
		a2.shape = (a2.rows(), 2 * a2.cols())
		a2._rref()
		for i in range(a2.rows()):
			a2.values[i] = a2.values[i][a2.cols() // 2:]
		a2.shape = (a2.rows(), a2.cols() // 2)
		id2 = self.matmul(a2)
		if id == id2:
			return a2
		raise ValueError('matrix is not invertible.')

	def matmul(self, m):
		if self.cols() != m.rows():
			raise self.InvalidShapeError
		return Matrix([[sum(x * y for x, y in zip(r1, r2)) for r2 in zip(*m.values)] for r1 in self.values])

	def transpose(self):
		return Matrix([[self.values[j][i] for j in range(self.rows())] for i in range(self.cols())])

	def __add__(self, m):
		return self._do_op(m, lambda x, y: x + y)

	def __eq__(self, m):
		if not isinstance(m, Matrix) or self.shape != m.shape:
			return False
		return all(all(is_close(x, y) for x, y in zip(r1, r2)) for r1, r2 in zip(self.values, m.values))

	def __mod__(self, m):
		return self._do_op(m, lambda x, y: x % y)

	def __mul__(self, m):
		return self._do_op(m, lambda x, y: x * y)

	def __ne__(self, m):
		return not self == m

	def __neg__(self):
		return Matrix([[-x for x in r] for r in self.values])

	def __pos__(self):
		return self

	def __pow__(self, m):
		if self.rows() != self.cols():
			raise self.NotSquareError
		if not isinstance(m, int):
			raise TypeError('exponent must be an integer.')
		if m < 0:
			raise ValueError('exponent must be non-negative.')
		if m == 0:
			return Matrix.identity(self.rows(), dtype=type(self.values[0][0]))
		if m == 1:
			return self
		return self.matmul(self ** (m - 1))

	def __radd__(self, m):
		return self + m

	def __repr__(self):
		return f"Matrix({self.values})"

	def __rmul__(self, m):
		return self * m

	def __rsub__(self, m):
		return self._do_op(m, lambda x, y: y - x)

	def __str__(self):
		rows = '; '.join('[' + ', '.join(str(e) for e in row) + ']' for row in self.values)
		return '[' + rows + ']'

	def __sub__(self, other):
		return self._do_op(other, lambda x, y: x - y)

	def __truediv__(self, other):
		return self._do_op(other, lambda x, y: x / y)

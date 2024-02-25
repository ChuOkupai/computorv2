from math import sqrt
from src.dtype import unsupported_op

class Complex:
	pass

def _check_type(op, a, b):
	if isinstance(a, Complex):
		return a
	if isinstance(a, (float, int)):
		return Complex(a)
	raise unsupported_op(op, a, b)

class Complex:
	def __init__(self, real: float, imag: float):
		self.real = real
		self.imag = imag

	def _try_convert_as_int(self):
		return [int(x) if x.is_integer() else x for x in [self.real, self.imag]]

	def __abs__(self):
		return sqrt(self.real ** 2 + self.imag ** 2)

	def __add__(self, c):
		c = _check_type('+', self, c)
		return Complex(self.real + c.real, self.imag + c.imag)

	def __mul__(self, c):
		c = _check_type('*', self, c)
		a, b, c, d = self.real, self.imag, c.real, c.imag
		return Complex(a * c - b * d, a * d + b * c)

	def __pos__(self):
		return self

	def __pow__(self, c):
		return NotImplementedError

	def __neg__(self):
		return Complex(-self.real, -self.imag)

	def __radd__(self, c):
		return self + _check_type('+', self, c)

	def __rmul__(self, c):
		return self * _check_type('*', self, c)

	def __rpow__(self, c):
		return NotImplementedError

	def __rsub__(self, c):
		return self._check_type(c, '-', True) - self

	def __rtruediv__(self, c):
		return _check_type('/', self, c) / self

	def __sub__(self, c):
		c = self._check_type(c, '-')
		return Complex(self.real - c.real, self.imag - c.imag)

	def __truediv__(self, c):
		c = _check_type('/', self, c)
		a, b, c, d = self.real, self.imag, c.real, c.imag
		c2d2 = c ** 2 + d ** 2
		return Complex((a * c + b * d) / c2d2, (b * c - a * d) / c2d2)

	def __str__(self):
		r, i = self._try_convert_as_int()
		if r:
			sign = f" {'+' if i >= 0 else '-'} "
		else:
			r = ''
			sign = '' if i >= 0 else '-'
		i = abs(i)
		return f"{r}{sign}{i if i != 1 else ''}i"

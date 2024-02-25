from copy import copy
from math import atan2, cos, sin, sqrt
from src.dtype import unsupported_op

class Complex:
	pass

class Complex:
	"""Represents a complex number."""

	def __init__(self, real=0.0, imag=0.0):
		for i, arg in enumerate([real, imag]):
			if not isinstance(arg, (float, int)):
				raise TypeError(f"Complex(): Argument {i + 1} must be a number.")
		self.real = float(real)
		self.imag = float(imag)

	def _check_type(self, c, op, reverse=False):
		if isinstance(c, Complex):
			return c
		if isinstance(c, (float, int)):
			return Complex(c)
		args = [c, self] if reverse else [self, c]
		raise unsupported_op(op, *args)

	def _try_convert_as_int(self):
		return [int(x) if x.is_integer() else x for x in [self.real, self.imag]]

	def __add__(self, c):
		c = self._check_type(c, '+')
		b = copy(self)
		b += c
		return b

	def __iadd__(self, c):
		c = self._check_type(c, '+=')
		self.real += c.real
		self.imag += c.imag
		return self

	def __radd__(self, c):
		return self + self._check_type(c, '+', True)

	def __sub__(self, c):
		c = self._check_type(c, '-')
		b = copy(self)
		b -= c
		return b

	def __isub__(self, c):
		c = self._check_type(c, '-=')
		self.real -= c.real
		self.imag -= c.imag
		return self

	def __rsub__(self, c):
		c = self._check_type(c, '-', True)
		b = -copy(self)
		b += c
		return b

	def __mul__(self, c):
		c = self._check_type(c, '*')
		b = copy(self)
		b *= c
		return b

	def __imul__(self, c):
		c = self._check_type(c, '*=')
		a, b, c, d = self.real, self.imag, c.real, c.imag
		self.real = a * c - b * d
		self.imag = a * d + b * c
		return self

	def __rmul__(self, c):
		return self * self._check_type(c, '*', True)

	def __truediv__(self, c):
		c = self._check_type(c, '/')
		b = copy(self)
		b /= c
		return b

	def __itruediv__(self, c):
		c = self._check_type(c, '/=')
		a, b, c, d = self.real, self.imag, c.real, c.imag
		c2d2 = c ** 2 + d ** 2
		self.real = (a * c + b * d) / c2d2
		self.imag = (b * c - a * d) / c2d2
		return self

	def __rtruediv__(self, c):
		return self._check_type(c, '/', True) / self

	def __neg__(self):
		return Complex(-self.real, -self.imag)

	def __pos__(self):
		return self

	def __abs__(self):
		return sqrt(self.real ** 2 + self.imag ** 2)

	def __pow__(self, c):
		return NotImplementedError

	def __ipow__(self, c):
		return NotImplementedError

	def __rpow__(self, c):
		return NotImplementedError

	def __eq__(self, o):
		if isinstance(o, Complex):
			return self.real == o.real and self.imag == o.imag
		if isinstance(o, (float, int)):
			return self.real == o and self.imag == 0
		return False

	def __ne__(self, o):
		return not (self == o)

	def __hash__(self):
		key = (self.real, self.imag)
		return hash(key)

	def __repr__(self):
		r, i = self._try_convert_as_int()
		s = 'Complex('
		if r:
			s += str(r)
		if i:
			s += ', ' if r else ''
			s += str(i)
		return s + ')'

	def __str__(self):
		r, i = self._try_convert_as_int()
		if r:
			sign = f" {'+' if i >= 0 else '-'} "
		else:
			r = ''
			sign = '' if i >= 0 else '-'
		i = abs(i)
		return f"{r}{sign}{i if i != 1 else ''}i"

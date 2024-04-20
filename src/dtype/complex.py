from math import atan2, cos, exp, hypot, log, sin, sqrt
import src.dtype.matrix as dtype
import src.dtype.utils as utils

class Complex:
	pass

def implicit_conversion(func):
	def wrapper(self, c):
		if not isinstance(c, Complex):
			c = Complex(c)
		return func(self, c)
	return wrapper

class Complex:
	"""Represents a complex number."""

	def __init__(self, real=0, imag=0):
		self.real = float(real)
		self.imag = float(imag)

	def __abs__(self):
		return sqrt(self.real ** 2 + self.imag ** 2)

	def __add__(self, c):
		if isinstance(c, dtype.Matrix):
			return c + self
		if not isinstance(c, Complex):
			c = Complex(c)
		return Complex(self.real + c.real, self.imag + c.imag)

	def __eq__(self, c):
		if isinstance(c, Complex):
			return self.real == c.real and self.imag == c.imag
		if isinstance(c, (float, int)):
			return self.real == c and self.imag == 0
		return False

	def __mul__(self, c):
		if isinstance(c, dtype.Matrix):
			return c * self
		if not isinstance(c, Complex):
			c = Complex(c)
		a, b, c, d = self.real, self.imag, c.real, c.imag
		return Complex(a * c - b * d, a * d + b * c)

	def __ne__(self, c):
		return not self == c

	def __neg__(self):
		return Complex(-self.real, -self.imag)

	def __pos__(self):
		return self

	@implicit_conversion
	def __pow__(self, c):
		a, b = self, c
		if b == 0:
			return Complex(1)
		elif a == 0:
			if b.imag or b.real < 0:
				raise ZeroDivisionError
			return Complex()
		vabs = hypot(a.real, a.imag)
		vlen = vabs ** b.real
		at = atan2(a.imag, a.real)
		ph = at * b.real
		if b.imag:
			vlen /= exp(b.imag * at)
			ph += b.imag * log(vabs)
		a, b = vlen * cos(ph), vlen * sin(ph)
		a, b = [round(x) if utils.is_close(x, round(x), 1e-12) else x for x in [a, b]]
		return Complex(a, b) if b else Complex(a)

	def __radd__(self, c):
		return self + c

	def __repr__(self):
		args = [utils.try_cast_as_int(arg) for arg in [self.real, self.imag]]
		while len(args) and args[-1] == 0:
			args.pop()
		return f"Complex({', '.join(map(str, args))})"

	def __rmul__(self, c):
		return self * c

	@implicit_conversion
	def __rpow__(self, c):
		return c ** self

	@implicit_conversion
	def __rsub__(self, c):
		return c - self

	@implicit_conversion
	def __rtruediv__(self, c):
		return c / self

	def __str__(self):
		r, i = [utils.try_cast_as_int(x) for x in [self.real, self.imag]]
		if r:
			sign = f" {'+' if i >= 0 else '-'} "
		else:
			r = ''
			sign = '' if i >= 0 else '-'
		i = abs(i)
		return f"{r}{sign}{i if i != 1 else ''}i"

	def __sub__(self, c):
		if isinstance(c, dtype.Matrix):
			return -c + self
		if not isinstance(c, Complex):
			c = Complex(c)
		return Complex(self.real - c.real, self.imag - c.imag)

	@implicit_conversion
	def __truediv__(self, c):
		a, b, c, d = self.real, self.imag, c.real, c.imag
		c2d2 = c ** 2 + d ** 2
		return Complex((a * c + b * d) / c2d2, (b * c - a * d) / c2d2)

import math
from src.dtype.complex import Complex

def is_close(x, y, abs_tol=1e-9):
	if isinstance(x, Complex):
		return abs(x - y) < abs_tol
	return math.isclose(x, y, abs_tol=abs_tol)

def is_literal(x):
	"""Returns True if x is a literal, False otherwise."""
	return isinstance(x, (Complex, float, int))

def try_cast_as_int(x):
	return int(x) if isinstance(x, float) and x.is_integer() else x

class Polynomial:
	def __init__(self, terms = {}):
		"""Initialize a polynomial with the given terms.
		terms[0] is the constant term, terms[1] is the coefficient of X, etc."""
		self.terms = terms.copy()

	def __add__(self, other):
		"""Add two polynomials."""
		p = Polynomial(self.terms.copy())
		[p.add_coefficient(coeff, deg) for deg, coeff in other.terms.items()]
		return p

	def __eq__(self, other):
		"""Check if two polynomials are equal."""
		return self.terms == other.terms

	def __neg__(self):
		return Polynomial({deg: -self.terms[deg] for deg in self.terms})

	def __repr__(self):
		return f'Polynomial({self.terms})'

	def __str__(self):
		"""Return a string representation of the polynomial."""
		return str(self.terms)

	def __sub__(self, other):
		return self + (-other)

	def add_coefficient(self, coeff, degree):
		"""Add the given coefficient to the coefficient of the given degree."""
		if degree in self.terms:
			self.terms[degree] += coeff
		else:
			self.terms[degree] = coeff
		if self.terms[degree] == 0:
			self.terms.pop(degree)

	def get_coefficient(self, degree):
		"""Return the coefficient of the given degree."""
		return self.terms.get(degree, 0)

	def get_degree(self):
		"""Return the degree of the polynomial."""
		return max(self.terms.keys(), default=0)

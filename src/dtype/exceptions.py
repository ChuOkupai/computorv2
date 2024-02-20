class InvalidShapeError(ValueError):
	def __init__(self):
		super().__init__("Invalid shape")

class NotSquareError(ValueError):
	def __init__(self):
		super().__init__("Matrix is not square")

def unsupported_op(op, *args):
	"""Returns a TypeError for an unsupported operand.

	Arguments:
	op -- the unsupported operand
	*args -- the arguments passed to the operand
	"""
	args = list(map(lambda x: f"'{type(x).__name__}'", args))
	raise TypeError(f"unsupported operand type(s) for {op}: {' and '.join(args)}")

class InvalidShapeError(ValueError):
	def __init__(self):
		super().__init__("invalid matrix shape.")

class NotSquareError(ValueError):
	def __init__(self):
		super().__init__("matrix is not square.")

def unsupported_op(op, *args):
	args = list(map(lambda x: f"'{type(x).__name__}'", args))
	raise TypeError(f"unsupported operand type(s) for {op}: {' and '.join(args)}")

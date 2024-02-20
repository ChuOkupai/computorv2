from src.ast import Ast, BinaryOp, Constant, FunCall, FunDecl, Identifier, MatDecl, UnaryOp, VarDecl, Visitor
from src.dtype import Matrix
from src.interpreter.storage import Storage


class EvalVisitor(Visitor):
	"""Evaluates the AST using the given storage."""

	def __init__(self, storage: Storage):
		self.res = None
		self.storage = storage

	def visit(self, root: Ast):
		root.accept(self)
		return self.res

	def visit_constant(self, constant: Constant) -> None:
		self.res = constant.value

	def visit_identifier(self, id: Identifier) -> None:
		self.res = self.storage.get_variable(id.name)
		if not self.res:
			raise NameError(f'Variable {id.name} is not defined')

	def visit_vardecl(self, vardecl: VarDecl) -> None:
		name = vardecl.name.name
		vardecl.value.accept(self)
		value = self.res
		self.storage.set_variable(name, value)

	def visit_matdecl(self, matdecl: MatDecl) -> None:
		values = []
		for row in matdecl.rows:
			row_values = []
			for cell in row:
				cell.accept(self)
				row_values.append(self.res)
			values.append(row_values)
		self.res = Matrix(values)

	def visit_fundecl(self, fundecl: FunDecl) -> None:
		raise NotImplementedError('Function declarations are not supported yet')

	def visit_funcall(self, funcall: FunCall) -> None:
		raise NotImplementedError('Function calls are not supported yet')

	def visit_binaryop(self, binop: BinaryOp) -> None:
		do_ops = {
			'+': lambda a, b: a + b,
			'/': lambda a, b: a / b,
			'%': lambda a, b: a % b,
			'*': lambda a, b: a * b,
			'^': lambda a, b: a ** b,
			'-': lambda a, b: a - b
		}
		binop.left.accept(self)
		left = self.res
		binop.right.accept(self)
		right = self.res
		self.res = do_ops[binop.op](left, right)

	def visit_unaryop(self, unop: UnaryOp) -> None:
		do_ops = { '-': lambda a: -a, '+': lambda a: a }
		unop.right.accept(self)
		right = self.res
		self.res = do_ops[unop.op](right)

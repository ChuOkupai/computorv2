from src.ast import Assign, Ast, BinaryOp, Constant, FunCall, Identifier, MatDecl, Solve, \
	UnaryOp, Visitor
from src.interpreter import Context

class OptimizerVisitor(Visitor):
	"""Optimizes the AST by evaluating constant expressions and removing useless nodes."""

	def __init__(self, ctx: Context):
		self.res = None
		self.ctx = ctx

	def visit(self, node: Ast):
		node.accept(self)
		return self.res

	def visit_assign(self, assign: Assign):
		assign.target = self.visit(assign.target)
		assign.value = self.visit(assign.value)
		self.res = assign

	def visit_binaryop(self, binop: BinaryOp):
		binop.left = self.visit(binop.left)
		binop.right = self.visit(binop.right)
		if isinstance(binop.right, Constant) and '+-'.find(binop.op) >= 0 and \
			isinstance(binop.right.value, (int, float)) and binop.right.value < 0:
			print("Rule E", binop.op, "-F -> E", '-' if binop.op == '+' else '+', "F")
			binop.op = '-' if binop.op == '+' else '+'
			binop.right.value = -binop.right.value
			self.res = binop
		left_const = isinstance(binop.left, Constant)
		right_const = isinstance(binop.right, Constant)
		if left_const and right_const:
			print("Rule E", binop.op, "E -> const")
			self.res = Constant(binop.evaluate(binop.left.value, binop.right.value))
			self.res = self.visit(self.res)
			return
		lop = binop.left
		if right_const and isinstance(lop, BinaryOp) and \
			(isinstance(lop.left, Constant) or isinstance(lop.right, Constant)) and \
			(('+-'.find(binop.op) >= 0 and '+-'.find(lop.op) >= 0) or \
			('*/'.find(binop.op) >= 0 and '*/'.find(lop.op) >= 0)):
			if isinstance(lop.left, Constant) and '-/'.find(lop.op) < 0:
				lop.left, lop.right = lop.right, lop.left
			# Right tree rotation
			self.res = binop.left
			binop.left = self.res.right
			self.res.right = binop
			self.visit(self.res)
			return
		if (binop.op == '+' or binop.op == '*') and (left_const or right_const):
			if left_const and not right_const:
				# Reorder the expression to E op const
				binop.left, binop.right = binop.right, binop.left
			if binop.right.value == 0:
				if binop.op == '+':
					print("Rule E + 0 -> E")
					self.res = binop.left
					return
				elif binop.op == '*':
					print("Rule 0 * E -> 0")
					self.res = Constant(0)
					return
			elif binop.op == '*':
				if binop.right.value == 1:
					print("Rule 1 * E -> E")
					self.res = binop.left
					return
				# Reorder the expression to const * E
				binop.left, binop.right = binop.right, binop.left
		elif binop.op == '-':
			if right_const and binop.right.value == 0:
				print("Rule E - 0 -> E")
				self.res = binop.left
				return
			elif left_const and binop.left.value == 0:
				print("Rule 0 - E -> -E")
				self.res = UnaryOp('-', binop.right)
				return
		elif binop.op == '/':
			if right_const and binop.right.value == 1:
				print("Rule E / 1 -> E")
				self.res = binop.left
				return
		elif binop.op == '^':
			if right_const and binop.right.value == 0:
				print("Rule E ^ 0 -> 1")
				# TODO: Check if the left operand is a matrix (must be identity if square matrix)
				self.res = Constant(1)
				return
			elif right_const and binop.right.value == 1:
				print("Rule E ^ 1 -> E")
				self.res = binop.left
				return
		self.res = binop

	def visit_constant(self, constant: Constant):
		self.res = constant

	def visit_funcall(self, funcall: FunCall):
		funcall.args = [self.visit(arg) for arg in funcall.args]
		self.res = funcall

	def visit_identifier(self, id: Identifier):
		self.res = id

	def visit_matdecl(self, matdecl: MatDecl):
		matdecl.rows = [[self.visit(cell) for cell in row] for row in matdecl.rows]
		self.res = matdecl

	def visit_solve(self, solve: Solve):
		solve.assign = self.visit(solve.assign)
		self.res = solve

	def visit_unaryop(self, unop: UnaryOp):
		unop.right = self.visit(unop.right)
		if unop.op == '+':
			print("Rule + E -> E")
			self.res = unop.right
		elif isinstance(unop.right, UnaryOp):
			print("Rule - - E -> E")
			self.res = unop.right.right
		else:
			self.res = unop

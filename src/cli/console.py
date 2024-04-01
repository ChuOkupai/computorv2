import os, readline, sys, traceback
from src.ast import Ast, RenderVisitor
from src.cli import Completer
from src.interpreter import AnalyzerVisitor, Context, EvaluatorVisitor, InterpreterErrorGroup, \
	OptimizerVisitor
from src.parser import parse

class Console():
	def __init__(self, histfile: str, histsize: int):
		readline.parse_and_bind("tab: complete")
		readline.set_auto_history(False)
		readline.set_history_length(histsize)
		self.histfile = os.path.expanduser(histfile) if histfile else None
		if self.histfile:
			try:
				readline.read_history_file(self.histfile)
			except FileNotFoundError:
				pass
		self.ctx = Context()

	def _exec(self, ast: Ast):
		print('---> AST Dump')
		print(repr(ast))
		print('---> AST Render')
		print(RenderVisitor().visit(ast))
		print('---> AST Analyzer')
		AnalyzerVisitor(self.ctx).visit(ast)
		print('---> AST Evaluator')
		ast = EvaluatorVisitor(self.ctx).visit(ast)
		print('---> AST Optimizer')
		ast = OptimizerVisitor(self.ctx).visit(ast)
		print('---> Result')
		print(repr(ast))
		print(RenderVisitor().visit(ast))

	def _save_history(self):
		if self.histfile:
			try:
				readline.write_history_file(self.histfile)
			except Exception as e:
				print('error saving history:', e, file=sys.stderr)

	def _update_completer(self):
		completer = Completer(self.ctx.get_all_symbols())
		readline.set_completer(completer.complete)

	def run(self):
		buf = ''
		self._update_completer()
		while True:
			line = ''
			try:
				line = input('... ' if buf else '> ')
				if not line:
					continue
			except EOFError:
				break
			readline.add_history(line)
			buf += line + '\n'
			try:
				self._exec(parse(buf))
				self._update_completer()
			except EOFError:
				continue
			except InterpreterErrorGroup as e:
				for i in e.errors:
					print(i)
			except Exception as e:
				traceback.print_exc()
				if isinstance(e.args[0],list):
					for i in e.args[0]:
						print(i)
			buf = ''
		self._save_history()

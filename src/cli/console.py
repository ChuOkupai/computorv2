import os, readline, sys
from src.ast import Ast, RenderVisitor
from src.cli import Completer
from src.interpreter import AnalyzerVisitor, Context, EvaluatorVisitor, InterpreterErrorGroup
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
		AnalyzerVisitor(self.ctx).visit(ast)
		ast = EvaluatorVisitor(self.ctx).visit(ast)
		if ast:
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
				if sys.stdin.isatty():
					prompt = '... ' if buf else '> '
				else:
					prompt = ''
				line = input(prompt)
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
				if isinstance(e.args[0],list):
					for i in e.args[0]:
						print(i)
				else:
					print(e)
			buf = ''
		self._save_history()

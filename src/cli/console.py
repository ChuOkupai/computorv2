import os, readline, sys
from src.ast import Ast, RenderVisitor
from src.cli import Completer
from src.interpreter import AnalyzerVisitor, Context, EvaluatorVisitor, InterpreterErrorGroup, \
	RemovedFunctionError
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

	colors = {
		'black': '\033[30m',
		'red': '\033[31m',
		'green': '\033[32m',
		'yellow': '\033[33m',
		'blue': '\033[34m',
		'magenta': '\033[35m',
		'cyan': '\033[36m',
		'white': '\033[37m',
		'bright_black': '\033[90m',
		'bright_red': '\033[91m',
		'bright_green': '\033[92m',
		'bright_yellow': '\033[93m',
		'bright_blue': '\033[94m',
		'bright_magenta': '\033[95m',
		'bright_cyan': '\033[96m',
		'bright_white': '\033[97m',
		'end': '\033[0m'
	}

	def _exec(self, ast: Ast):
		AnalyzerVisitor(self.ctx).visit(ast)
		ast = EvaluatorVisitor(self.ctx).visit(ast)
		if ast:
			print(RenderVisitor().visit(ast))

	def _print_errors(self, errors: list):
		for err in errors:
			if isinstance(err, RemovedFunctionError):
				color = Console.colors['bright_magenta']
				etype= 'warning'
			else:
				color = Console.colors['bright_red']
				etype = 'error'
			print(f"{color}{etype}:{Console.colors['end']} {err}", file=sys.stderr)

	def _save_history(self):
		if self.histfile:
			try:
				readline.write_history_file(self.histfile)
			except Exception as e:
				self._print_errors([e.args[0]])

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
				self._print_errors(e.errors)
			except Exception as e:
				if len(e.args) and isinstance(e.args[0], list):
					self._print_errors(e.args[0])
				else:
					self._print_errors([e.args[0]])
			buf = ''
		self._save_history()

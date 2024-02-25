import sys
from src.ast import RenderVisitor
from src.interpreter import EvalVisitor, Storage
from src.parser import parse, tokenize

if __name__ == '__main__':
	storage = Storage()
	contents = ''
	while True:
		try:
			line = input('... ' if contents else '> ')
			if not line:
				continue
		except EOFError:
			break
		contents += line + '\n'
		try:
			tokens = tokenize(contents)
			print('---> Tokens')
			print(tokens)
			ast = parse(contents)
			print('---> AST Dump')
			print(repr(ast))
			print(ast)
			print('---> AST Render')
			RenderVisitor().visit(ast)
			print('---> AST Eval')
			print(EvalVisitor(storage).visit(ast))
		except EOFError:
			continue
		except NameError as e:
			print("Name error:", e, file=sys.stderr)
		except NotImplementedError as e:
			print("Exec error:", e, file=sys.stderr)
		except SyntaxError as e:
			print("Syntax error:", e, file=sys.stderr)
		except TypeError as e:
			print("Type error:", e, file=sys.stderr)
		contents = ''

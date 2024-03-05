import traceback
from src.ast import RenderVisitor
from src.interpreter import Storage
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
			print('---> AST Render')
			print(RenderVisitor().visit(ast))
		except EOFError:
			continue
		except Exception as e:
			traceback.print_exc()
		contents = ''

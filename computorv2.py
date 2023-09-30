import sys
from src.parser import parser, parse, tokenize

if __name__ == '__main__':
	contents = ''
	while True:
		line = input('... ' if contents else '> ')
		contents += line + '\n'
		try:
			ast = parse(contents)
			print('---> AST Dump')
			print(repr(ast))
			print(ast)
		except EOFError:
			continue
		except SyntaxError as e:
			print("syntax error:", e, file=sys.stderr)
		contents = ''

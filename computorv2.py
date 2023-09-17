import sys
from src.parser import lexer, parser, parse, tokenize

if __name__ == '__main__':
	contents = ''
	while True:
		line = input('... ' if contents else '> ')
		contents += line + '\n'
		try:
			tokens = tokenize(contents)
			ast = parse(contents)
			for token in tokens:
				print(token)
			print(ast)
			parser.restart()
		except EOFError:
			continue
		except SyntaxError as e:
			print('Raised SyntaxError', file=sys.stderr)
			print(e, file=sys.stderr)
			exit(1)
		contents = ''

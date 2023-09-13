import sys
from src.lexer import tokenize

def get_user_input():
	contents = []
	while True:
		try:
			line = input()
		except EOFError:
			break
		contents.append(line)
	return '\n'.join(contents)

if __name__ == '__main__':
	contents = get_user_input()
	tokens = tokenize(contents)
	for token in tokens:
		print(token)

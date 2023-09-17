import sys
import ply.lex as lex

tokens = [
	# Simple tokens
		# Operators
	'DIV',
	'EQUALS',
	'MINUS',
	'MOD',
	'MULT',
	'PLUS',
	'POW',
		# Symbols
	'COMMA',
	'LBRACKET',
	'LPAREN',
	'QMARK',
	'RBRACKET',
	'RPAREN',
	'SEMICOL',

	# Complex tokens
	'FLOAT',
	'ID',
	'INT'
]

# Regular expression rules for simple tokens
	# Operators
t_DIV = r'\/'
t_EQUALS = r'='
t_MINUS = r'-'
t_MOD = r'%'
t_MULT = r'\*'
t_PLUS = r'\+'
t_POW = r'\^'
	# Symbols
t_COMMA = r','
t_LBRACKET = r'\['
t_LPAREN = r'\('
t_QMARK = r'\?'
t_RBRACKET = r'\]'
t_RPAREN = r'\)'
t_SEMICOL = r';'
	# Ignored characters
t_ignore_COMMENT = r'\#.*'
t_ignore_WHITESPACE = r'[^\S\r\n]+'

# Regular expression rules for complex tokens

def t_FLOAT(t):
	r'inf|(\d+\.\d*|\.\d+)([eE][-+]?\d+)?|(\d+[eE][-+]?\d+)'
	t.value = float(t.value)
	return t

def t_ID(t):
	r'[a-zA-Z]+'
	t.value = str(t.value)
	return t

def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

# Define a rule so we can track line numbers
def t_newline(t):
	r'[\r\n]+'
	t.lexer.lineno += len(t.value.replace('\r', ''))

# Error handling rule
def t_error(t):
	raise SyntaxError("Illegal character '%s' on line %d" % (t.value[0], t.lineno))

# Build the lexer
lexer = lex.lex()

def reset_lexer():
	lexer.lineno = 1

def tokenize(contents):
	reset_lexer()
	lexer.input(contents)
	tokens = []
	while True:
		token = lexer.token()
		if not token:
			break
		tokens.append(token)
	return tokens

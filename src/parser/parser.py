import ply.yacc as yacc
from src import ast
from src.parser.lexer import convert_to_binary_op, convert_to_unary_op, reset_lexer, tokens

precedence = (
	('left', 'ADD', 'SUB'),
	('left', 'MUL', 'DIV', 'MOD'),
	('left', 'POW'),
	('right', 'USUB', 'UADD'),
	('left', 'QMARK')
)

def p_statement(p):
	'''statement : expression
		| fun_decl
		| var_decl'''
	p[0] = p[1]

def p_expression(p):
	'''expression : terminal'''
	p[0] = p[1]

def p_terminal(p):
	'''terminal : constant
		| variable
		| matrix'''
	p[0] = p[1]

def p_constant(p):
	'''constant : FLOAT
		| INT'''
	p[0] = ast.Constant(p[1])

def p_variable(p):
	'''variable : ID'''
	p[0] = ast.Identifier(p[1])

def p_matrix(p):
	'''matrix : LBRACKET matrix_rows_list RBRACKET'''
	p[0] = p[2]

def p_matrix_rows_list(p):
	'''matrix_rows_list : matrix_row'''
	p[0] = p[1]

def p_matrix_rows_list_append(p):
	'''matrix_rows_list : matrix_rows_list SEMICOL matrix_row'''
	p[0] = p[1]
	p[0].append(p[3])

def p_matrix_row(p):
	'''matrix_row : expressions_list'''
	p[0] = p[1]

def p_expressions_list(p):
	'''expressions_list : expression'''
	p[0] = [p[1]]

def p_expression_list_append(p):
	'''expressions_list : expressions_list COMMA expression'''
	p[0] = p[1]
	p[0].append(p[3])

def p_expression_fun_call(p):
	'''expression : variable LPAREN expressions_list RPAREN'''
	p[0] = ast.FunCall(p[1], p[3])

def p_expression_binary_op(p):
	'''expression : expression ADD expression
		| expression DIV expression
		| expression MOD expression
		| expression MUL expression
		| expression POW expression
		| expression SUB expression'''
	p[0] = ast.BinaryOp(p[1], convert_to_binary_op(p[2]), p[3])

def p_expression_unary_op(p):
	'''expression : SUB expression %prec USUB
		| ADD expression %prec UADD'''
	p[0] = ast.UnaryOp(convert_to_unary_op(p[1]), p[2])

def p_expression_group(p):
	'''expression : LPAREN expression RPAREN'''
	p[0] = p[2]

def p_expression_implicit_mul(p):
	'''expression : terminal variable %prec MUL'''
	p[0] = ast.BinaryOp(p[1], ast.BinaryOpType.Mul, p[2])

def p_fun_decl(p):
	'''fun_decl : variable LPAREN expressions_list RPAREN EQUALS expression'''
	p[0] = ast.FunDecl(p[1], p[3], p[6])

def p_var_decl(p):
	'''var_decl : variable EQUALS expression'''
	p[0] = ast.VarDecl(p[1], p[3])

# Error rule for syntax errors
def p_error(p):
	if not p:
		raise EOFError("Unexpected end of file")
	raise SyntaxError("Syntax error near unexpected token '%s' on line %d" % (p.value, p.lineno))

# Instantiate the parser
parser = yacc.yacc()

def parse(s: str):
	if hasattr(parser, 'statestack'):
		parser.restart()
	reset_lexer()
	return parser.parse(s)

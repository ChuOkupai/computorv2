import ply.yacc as yacc
from src.parser import reset_lexer, tokens
from src import ast

precedence = (
	('left', 'QMARK'),
	('right', 'EQUALS'),
	('left', 'ADD', 'SUB'),
	('left', 'MUL', 'MATMUL', 'DIV', 'MOD'),
	('right', 'POW'),
	('right', 'UADD', 'USUB')
)

associativity_dict = { token: e[0] for e in precedence for token in e[1:] }
precedence_dict = { token: i for i, e in enumerate(precedence) for token in e[1:] }

def p_statement(p):
	'''statement : expr
		| fun_decl
		| var_decl'''
	p[0] = p[1]

def p_expr_group(p):
	'''expr : LPAREN expr RPAREN'''
	p[0] = p[2]

def p_expr_terminal(p):
	'''expr : constant
		| variable
		| matrix
		| fun_call'''
	p[0] = p[1]

def p_constant(p):
	'''constant : FLOAT
		| INT'''
	p[0] = ast.Constant(p[1])

def p_variable(p):
	'''variable : ID'''
	p[0] = ast.Identifier(p[1])

def p_expr_implicit_mul(p):
	'''expr : constant variable %prec MUL'''
	p[0] = ast.BinaryOp(p[1], '*', p[2])

def p_expr_binary_op(p):
	'''expr : expr ADD expr
		| expr DIV expr
		| expr MATMUL expr
		| expr MOD expr
		| expr MUL expr
		| expr POW expr
		| expr SUB expr'''
	p[0] = ast.BinaryOp(p[1], p[2], p[3])

def p_expr_unary_op(p):
	'''expr : ADD expr %prec UADD
		| SUB expr %prec USUB'''
	p[0] = ast.UnaryOp(p[1], p[2])

def p_matrix(p):
	'''matrix : LBRACKET matrix_rows RBRACKET'''
	p[0] = ast.MatDecl(p[2])

def p_matrix_rows(p):
	'''matrix_rows : matrix_row'''
	p[0] = [p[1]]

def p_matrix_rows_append(p):
	'''matrix_rows : matrix_rows SEMICOL matrix_row'''
	p[0] = p[1]
	p[0].append(p[3])

def p_matrix_row(p):
	'''matrix_row : LBRACKET arguments RBRACKET'''
	p[0] = p[2]

def p_arguments(p):
	'''arguments : expr'''
	p[0] = [p[1]]

def p_arguments_append(p):
	'''arguments : arguments COMMA expr'''
	p[0] = p[1]
	p[0].append(p[3])

def p_fun_call(p):
	'''fun_call : variable LPAREN arguments RPAREN'''
	p[0] = ast.FunCall(p[1], p[3])

def p_fun_decl(p):
	'''fun_decl : fun_call EQUALS expr'''
	p[0] = ast.FunDecl(p[1].id, p[1].args, p[3])

def p_var_decl(p):
	'''var_decl : variable EQUALS expr'''
	p[0] = ast.VarDecl(p[1], p[3])

# Error rule for syntax errors
def p_error(p):
	if not p:
		raise EOFError("Unexpected end of file")
	raise SyntaxError("Syntax error near unexpected token '%s' on line %d" % (p.value, p.lineno))

parser = yacc.yacc()

def parse(s: str):
	if hasattr(parser, 'statestack'):
		parser.restart()
	reset_lexer()
	return parser.parse(s)

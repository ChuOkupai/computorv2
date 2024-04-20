import ply.yacc as yacc
from src.parser import reset_lexer, tokens
from src import ast

precedence = (
	('left', 'ADD', 'SUB'),
	('left', 'MATMUL'),
	('left', 'MUL', 'DIV', 'MOD'),
	('right', 'POW'),
	('right', 'UADD', 'USUB'),
)

associativity_dict = { token: e[0] for e in precedence for token in e[1:] }
precedence_dict = { token: i for i, e in enumerate(precedence) for token in e[1:] }

def p_statement(p):
	'''statement : eval
		| assign
		| solve
		| cmd'''
	p[0] = p[1]

def p_eval(p):
	'''eval : expr
		| expr EQUALS QMARK'''
	p[0] = p[1]

def p_expr(p):
	'''expr : constant
		| identifier
		| mat_decl
		| fun_call'''
	p[0] = p[1]

def p_constant(p):
	'''constant : FLOAT
		| INT'''
	p[0] = ast.Constant(p[1])

def p_identifier(p):
	'''identifier : ID'''
	p[0] = ast.Identifier(p[1].lower())

def p_expr_binary_op(p):
	'''expr : expr ADD expr
		| expr DIV expr
		| expr MATMUL expr
		| expr MOD expr
		| expr MUL expr
		| expr POW expr
		| expr SUB expr'''
	p[0] = ast.BinaryOp(*p[1:])

def p_expr_implicit_mul(p):
	'''expr : constant identifier
		| mat_decl identifier'''
	p[0] = ast.BinaryOp(p[1], '*', p[2])

def p_expr_group(p):
	'''expr : LPAREN expr RPAREN'''
	p[0] = p[2]

def p_expr_unary_op(p):
	'''expr : signed_expr'''
	p[0] = p[1]

def p_signed_expr(p):
	'''signed_expr : ADD expr %prec UADD
		| SUB expr %prec USUB'''
	p[0] = ast.UnaryOp(p[1], p[2])

def p_mat_decl(p):
	'''mat_decl : LBRACKET mat_decl_rows RBRACKET'''
	p[0] = ast.MatDecl(p[2])

def p_mat_decl_rows(p):
	'''mat_decl_rows : mat_decl_row'''
	p[0] = [p[1]]

def p_mat_decl_rows_append(p):
	'''mat_decl_rows : mat_decl_rows SEMICOL mat_decl_row'''
	p[0] = p[1]
	p[0].append(p[3])

def p_mat_decl_row(p):
	'''mat_decl_row : LBRACKET expr_list RBRACKET'''
	p[0] = p[2]

def p_expr_list(p):
	'''expr_list : expr'''
	p[0] = [p[1]]

def p_expr_list_append(p):
	'''expr_list : expr_list COMMA expr'''
	p[0] = p[1]
	p[0].append(p[3])

def p_fun_call(p):
	'''fun_call : identifier LPAREN expr_list RPAREN'''
	p[0] = ast.FunCall(p[1], p[3])

def p_assign(p):
	'''assign : expr EQUALS expr'''
	p[0] = ast.Assign(p[1], p[3])

def p_solve(p):
	'''solve : assign QMARK'''
	p[0] = ast.Solve(p[1])

def p_cmd(p):
	'''cmd : MOD cmd_args'''
	p[0] = ast.Command(p[2])

def p_cmd_args(p):
	'''cmd_args : cmd_arg'''
	p[0] = [p[1]]

def p_cmd_args_append(p):
	'''cmd_args : cmd_args cmd_arg'''
	p[0] = p[1]
	p[0].append(p[2])

def p_cmd_arg(p):
	'''cmd_arg : ID'''
	p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
	if not p:
		raise EOFError("unexpected end of file")
	raise SyntaxError("syntax error near unexpected token '%s' on line %d" % (p.value, p.lineno))

parser = yacc.yacc()

def parse(s: str):
	if hasattr(parser, 'statestack'):
		parser.restart()
	reset_lexer()
	return parser.parse(s)

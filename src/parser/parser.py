import ply.yacc as yacc
from src.ast import Ast, Constant, VarDecl, Variable
from src.parser import reset_lexer, tokens

precedence = (
)

def p_statement(p):
	'''statement : var_decl'''
	p[0] = p[1]

def p_var_decl(p):
	'''var_decl : variable EQUALS litteral'''
	p[0] = VarDecl(p.lineno(1), p.lexpos(1), p[1], p[3])

def p_litteral(p):
	'''litteral : constant
		| variable'''
	p[0] = p[1]

def p_constant(p):
	'''constant : FLOAT
		| INT'''
	p[0] = Constant(p.lineno(1), p.lexpos(1), p[1])

def p_variable(p):
	'''variable : ID'''
	p[0] = Variable(p.lineno(1), p.lexpos(1), p[1])

# Error rule for syntax errors
def p_error(p):
	if not p:
		raise EOFError("Unexpected end of file")
	raise SyntaxError("Syntax error near unexpected token '%s' on line %d" % (p.value, p.lineno))

# Instantiate the parser
parser = yacc.yacc()

def parse(s: str):
	reset_lexer()
	return parser.parse(s)

import traceback
from src.ast import RenderVisitor
from src.interpreter import AnalyzerVisitor, Context, EvaluatorVisitor, InterpreterErrorGroup
from src.parser import parse, tokenize

if __name__ == '__main__':
	ctx = Context()
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
			print('---> AST Analyzer')
			AnalyzerVisitor(ctx).visit(ast)
			print('---> AST Evaluator')
			ast = EvaluatorVisitor(ctx).visit(ast)
			print('---> Result')
			print(RenderVisitor().visit(ast))
		except EOFError:
			continue
		except InterpreterErrorGroup as e:
			for i in e.errors:
				print(i)
		except Exception as e:
			traceback.print_exc()
			if isinstance(e.args[0],list):
				for i in e.args[0]:
					print(i)
		contents = ''

import sys
from src.cli import Console

if __name__ == '__main__':
	histfile = "~/.computorv2_history" if sys.stdin.isatty() else None
	histsize = 1000 if histfile else 0
	try:
		console = Console(histfile, histsize)
		console.run()
	except Exception as e:
		print(e, file=sys.stderr)

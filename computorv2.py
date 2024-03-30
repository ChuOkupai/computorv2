import sys
from src.cli import Console

if __name__ == '__main__':
	histfile = "~/.computorv2_history" if sys.stdin.isatty() else None
	hostsize = 1000 if histfile else 0
	console = Console(histfile, hostsize)
	console.run()

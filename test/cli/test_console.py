import contextlib, io, os, sys, unittest
from src.cli import Console

class TestConsole(unittest.TestCase):
	"""Test the Console class."""

def create_test(in_file, out_file):
	def test(self):
		path = "test/cli/"
		with open(os.path.join(path, 'in', in_file), 'r') as in_f, \
			open(os.path.join(path, 'out', out_file), 'r') as out_f, \
			io.StringIO() as buffer, \
			contextlib.redirect_stdout(buffer), \
			contextlib.redirect_stderr(buffer):
			original_stdin = sys.stdin
			sys.stdin = in_f
			console = Console(None, 0)
			console.run()
			sys.stdin = original_stdin
			buffer.seek(0)
			actual_output = buffer.read()
			expected_output = out_f.read()
			self.assertEqual(actual_output, expected_output)
	return test

path = "test/cli/"
subdirs = ["in", "out"]
in_files, out_files = [os.listdir(path + dir) for dir in subdirs]
for in_file, out_file in zip(in_files, out_files):
	test_name = f'test_{in_file}'
	test = create_test(in_file, out_file)
	setattr(TestConsole, test_name, test)

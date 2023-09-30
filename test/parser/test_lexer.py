import unittest
from src.parser import tokenize as tk

class TestLexer(unittest.TestCase):
	"""This class contains tests for the Complex class."""

	def test_operators(self):
		expected = ['ADD', 'DIV', 'EQUALS', 'MOD', 'MUL', 'POW', 'SUB']
		tokens = tk('+/=%*^-')
		for i, token in enumerate(tokens):
			self.assertEqual(token.type, expected[i])

	def test_symbols(self):
		expected = ['COMMA', 'LBRACKET', 'LPAREN', 'QMARK', 'RBRACKET', 'RPAREN', 'SEMICOL']
		tokens = tk(',[(?]);')
		for i, token in enumerate(tokens):
			self.assertEqual(token.type, expected[i])

	def test_float(self):
		self.assertEqual(tk('inf')[0].type, 'FLOAT')
		self.assertEqual(tk('1.0')[0].type, 'FLOAT')
		self.assertEqual(tk('.1')[0].type, 'FLOAT')
		self.assertEqual(tk('1.0e1')[0].type, 'FLOAT')
		self.assertEqual(tk('1.0E1')[0].type, 'FLOAT')
		self.assertEqual(tk('1.e+1')[0].type, 'FLOAT')
		self.assertEqual(tk('345.34e-2')[0].type, 'FLOAT')
		self.assertEqual(tk('42.')[0].type, 'FLOAT')
		self.assertEqual(tk('10e42')[0].type, 'FLOAT')
		self.assertEqual(tk('10E42')[0].type, 'FLOAT')
		self.assertEqual(tk('10e+42')[0].type, 'FLOAT')
		self.assertEqual(tk('10e-42')[0].type, 'FLOAT')

	def test_id(self):
		self.assertEqual(tk('varA')[0].type, 'ID')
		self.assertEqual(len(tk('TEST')), 1)

	def test_int(self):
		self.assertEqual(tk('1')[0].type, 'INT')
		self.assertEqual(tk('123')[0].type, 'INT')
		self.assertEqual(tk('1234567890')[0].type, 'INT')

	def test_comment(self):
		self.assertEqual(tk('# Hello World'), [])
		t = tk('1 # Hello World')
		self.assertEqual(t[0].type, 'INT')
		self.assertEqual(len(t), 1)
		t = tk('1 # Hello World\n2')
		self.assertEqual(t[0].type, 'INT')
		self.assertEqual(t[1].type, 'INT')
		self.assertEqual(len(t), 2)

	def test_whitespace(self):
		self.assertEqual(tk(' '), [])
		self.assertEqual(tk('\t'), [])
		self.assertEqual(tk('\r'), [])
		self.assertEqual(tk('\n'), [])
		self.assertEqual(tk('\r\n'), [])
		self.assertEqual(tk(' \t\n\r'), [])
		self.assertEqual(len(tk(' \t\n\r1')), 1)

	def test_invalid(self):
		invalid_tokens = '!"$&\':<>@`|~'
		for t in invalid_tokens:
			self.assertRaises(Exception, tk, t)

	def test_integration(self):
		tokens = tk('varA = 1 - 3.5 * 4 / 5 ^ 6')
		expected = ['ID', 'EQUALS', 'INT', 'SUB', 'FLOAT', 'MUL', 'INT', 'DIV', 'INT', 'POW', 'INT']
		for i, token in enumerate(tokens):
			self.assertEqual(token.type, expected[i])

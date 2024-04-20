import unittest
from src.ast import *
from src.interpreter import ClearCommand, CommandError, Context, DeleteCommand, FunctionStorage, \
	HelpCommand, InvalidCommandError, ShowCommand, SystemCommandFactory

class TestSystemCommands(unittest.TestCase):
	"""This class tests the SystemCommandFactory class and its subclasses."""

	def setUp(self):
		self.ctx = Context()

	def test_clear(self):
		# This test is not very useful, but it is here for completeness.
		ClearCommand(None, ['clear']).execute()

	def test_delete(self):
		self.ctx.set_variable('a', 1)
		DeleteCommand(self.ctx, ['variable', 'a']).execute()
		self.assertIsNone(self.ctx.get_variable('a'))

	def test_delete_function(self):
		self.ctx.set_function('f', FunctionStorage([], []))
		DeleteCommand(self.ctx, ['function', 'f']).execute()
		self.assertIsNone(self.ctx.get_function('f'))

	def test_delete_function_builtin(self):
		with self.assertRaises(CommandError):
			DeleteCommand(self.ctx, ['function', 'sin']).execute()

	def test_delete_function_undefined(self):
		with self.assertRaises(CommandError):
			DeleteCommand(self.ctx, ['function', 'f']).execute()

	def test_delete_variable(self):
		self.ctx.set_variable('a', 1)
		DeleteCommand(self.ctx, ['variable', 'a']).execute()
		self.assertIsNone(self.ctx.get_variable('a'))

	def test_delete_variable_constant(self):
		with self.assertRaises(CommandError):
			DeleteCommand(self.ctx, ['variable', 'pi']).execute()

	def test_delete_variable_undefined(self):
		with self.assertRaises(CommandError):
			DeleteCommand(self.ctx, ['variable', 'a']).execute()

	def test_delete_invalid_command(self):
		with self.assertRaises(CommandError):
			DeleteCommand(None, []).execute()

	def test_delete_invalid_identifier(self):
		with self.assertRaises(CommandError):
			DeleteCommand(self.ctx, ['foo', 'bar']).execute()

	def test_help(self):
		HelpCommand(self.ctx, []).execute()

	def test_help_command(self):
		HelpCommand(self.ctx, ['delete']).execute()

	def test_help_invalid_command(self):
		with self.assertRaises(CommandError):
			HelpCommand(self.ctx, ['foo']).execute()

	def test_help_invalid_number_of_arguments(self):
		with self.assertRaises(CommandError):
			HelpCommand(self.ctx, ['delete', 'foo']).execute()

	def test_show(self):
		ShowCommand(self.ctx, []).execute()

	def test_show_all(self):
		ShowCommand(self.ctx, ['all']).execute()

	def test_show_functions(self):
		self.ctx.set_function('f', FunctionStorage([Identifier('x')], Constant(1)))
		ShowCommand(self.ctx, ['functions']).execute()

	def test_show_variables(self):
		self.ctx.set_variable('a', Constant(1))
		ShowCommand(self.ctx, ['variables']).execute()

	def test_show_invalid_command(self):
		with self.assertRaises(CommandError):
			ShowCommand(self.ctx, ['foo']).execute()

	def test_show_invalid_number_of_arguments(self):
		with self.assertRaises(CommandError):
			ShowCommand(self.ctx, ['all', 'foo']).execute()

	def test_system_command_factory(self):
		cmd = SystemCommandFactory.create(None, ['clear'])
		self.assertIsInstance(cmd, ClearCommand)

	def test_invalid_command(self):
		with self.assertRaises(InvalidCommandError):
			SystemCommandFactory.create(None, ['foo'])

import os
from abc import ABC, abstractmethod
from src.ast import RenderVisitor
from src.interpreter import CommandError, Context, InterpreterErrorGroup, InvalidCommandError, \
	RemovedFunctionError

class SystemCommand(ABC):
	"""Abstract class for system commands."""

	def __init__(self, ctx: Context, args: list):
		self.ctx = ctx
		self.args = args

	@abstractmethod
	def execute(self):
		"""Execute the command."""
		pass

class ClearCommand(SystemCommand):
	"""This command clears the screen."""

	def __init__(self, ctx: Context, args: list):
		super().__init__(ctx, args)

	def execute(self):
		os.system('cls' if os.name == 'nt' else 'clear')

class DeleteCommand(SystemCommand):
	"""This command deletes a function or a variable."""

	def __init__(self, ctx: Context, args: list):
		super().__init__(ctx, args)

	def _remove_functions_with_dependecy(self, dep_id: str):
		errors = []
		for id in self.ctx.get_functions_using_dependency(dep_id):
			errors += self._remove_functions_with_dependecy(id)
			errors.append(RemovedFunctionError(id, dep_id))
		self.ctx.unset_function(dep_id)
		return errors

	def execute(self):
		if len(self.args) != 2:
			raise CommandError('delete', 'invalid number of arguments')
		id_type, name = self.args
		if id_type == 'function':
			if self.ctx.is_builtin(name):
				raise CommandError('delete', f'cannot delete built-in function: {name}')
			if not self.ctx.get_function(name):
				raise CommandError('delete', f'undefined function: {name}')
			errors = self._remove_functions_with_dependecy(name)
			if errors:
				raise InterpreterErrorGroup(errors)
		elif id_type == 'variable':
			if self.ctx.is_constant(name):
				raise CommandError('delete', f'cannot delete built-in variable: {name}')
			if not self.ctx.get_variable(name):
				raise CommandError('delete', f'undefined variable: {name}')
			self.ctx.unset_variable(name)
		else:
			raise CommandError('delete', f'invalid identifier type: {id_type}')


class HelpCommand(SystemCommand):
	"""This command shows a help message."""

	commands_help = {
		'clear': ['Clear the screen.', ''],
		'delete': ['Delete a function or a variable.', '<function|variable> <name>'],
		'help': ['Show a help message.', '[command]'],
		'show': ['Show stored functions and/or variables.', '[all|functions|variables]']
	}

	def __init__(self, ctx: Context, args: list):
		super().__init__(ctx, args)

	def _show_help(self, command: str):
		if command not in self.commands_help:
			raise CommandError('help', f'unknown command: {command}')
		help_msg = self.commands_help[command]
		print(f'{command}: {help_msg[0]}')
		if help_msg[1]:
			print(f'Usage: {command} {help_msg[1]}')

	def execute(self):
		if len(self.args) > 1:
			raise CommandError('help', 'invalid number of arguments')
		elif len(self.args):
			self._show_help(self.args[0])
		else:
			print('Available commands:')
			[print(f'- {cmd}: {desc[0]}') for cmd, desc in self.commands_help.items()]


class ShowCommand(SystemCommand):
	"""This command shows stored functions and/or variables."""

	def __init__(self, ctx: Context, args: list):
		super().__init__(ctx, args)

	def _show_functions(self):
		functions = self.ctx.functions
		if not functions:
			print('No functions stored.')
		else:
			for id, fs in functions.items():
				args = ', '.join([RenderVisitor().visit(arg) for arg in fs.args])
				body = RenderVisitor().visit(fs.body)
				print(f'{id}({args}) = {body}')

	def _show_variables(self):
		variables = self.ctx.scopes[-1].variables
		if not variables:
			print('No variables stored.')
		else:
			[print(f'{id} = {RenderVisitor().visit(val)}') for id, val in variables.items()]

	def _show_all(self):
		self._show_functions()
		self._show_variables()

	def execute(self):
		if len(self.args) > 1:
			raise CommandError('show', 'invalid number of arguments')
		elif len(self.args):
			if self.args[0] == 'all':
				self._show_all()
			elif self.args[0] == 'functions':
				self._show_functions()
			elif self.args[0] == 'variables':
				self._show_variables()
			else:
				raise CommandError('show', 'invalid argument')
		else:
			self._show_all()

class SystemCommandFactory():
	"""Factory for creating system commands."""

	commands = {
		'clear': ClearCommand,
		'delete': DeleteCommand,
		'help': HelpCommand,
		'show': ShowCommand
	}

	@staticmethod
	def create(ctx: Context, args: list):
		name, args = args[0], args[1:]
		if name not in SystemCommandFactory.commands:
			raise InvalidCommandError(name)
		return SystemCommandFactory.commands[name](ctx, args)

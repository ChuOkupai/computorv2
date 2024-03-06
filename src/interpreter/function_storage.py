from dataclasses import dataclass
from src.ast import Ast

@dataclass
class FunctionStorage:
	args: list
	body: Ast

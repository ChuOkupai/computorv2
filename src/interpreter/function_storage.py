from dataclasses import dataclass, field
from src.ast import Ast

@dataclass
class FunctionStorage:
	args: list
	body: Ast
	dependencies: set = field(default_factory=set)

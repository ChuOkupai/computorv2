from dataclasses import dataclass

@dataclass
class Scope:
	id: str
	variables: dict

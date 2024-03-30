class Completer:
	def __init__(self, options):
		self.options = sorted(options)

	def _build_matches(self, text):
		if text:
			self.matches = [e for e in self.options if e.startswith(text)]
		else:
			self.matches = self.options[:]

	def complete(self, text, state):
		if state == 0:
			self._build_matches(text)
		return self.matches[state] if state < len(self.matches) else None

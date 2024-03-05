clean:
	find . -type d -name '__pycache__' |  xargs $(RM) -r
	$(RM) src/parser/parser.out src/parser/parsetab.py .coverage coverage.xml

coverage:
	coverage run -m unittest
	coverage xml
	coverage report --skip-covered --sort cover

run:
	python3 computorv2.py

test:
	python3 -m unittest

.PHONY: clean coverage run test

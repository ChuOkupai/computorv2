TEST_ARGS := -m unittest -b

all: coverage run

clean:
	find . -type d -name '__pycache__' |  xargs $(RM) -r
	$(RM) src/parser/parser.out src/parser/parsetab.py .coverage coverage.xml

coverage:
	coverage run $(TEST_ARGS)
	coverage xml
	coverage report --skip-covered --sort cover

run:
	python3 computorv2.py

test:
	python3 $(TEST_ARGS)

.PHONY: all clean coverage run test

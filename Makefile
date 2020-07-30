# convenience makefile to test a recipe

pep8_ignores = E501

prerequisites:
	pip install pep8 pyflakes

install: prerequisites

tests:
	python setup.py test
	pyflakes collective/
	pep8 --ignore=$(pep8_ignores) collective/

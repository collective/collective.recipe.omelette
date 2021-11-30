# convenience makefile to test a recipe

pep8_ignores = E501

prerequisites:
	pip install -r requirements.txt 

install: prerequisites

tests:
	tox

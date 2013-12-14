
all: run_tests

run_tests:
	python tests/unittest_runner.py

docs: locaudio/*
	doxygen Doxyfile



all: run_tests

run_tests:
	python tests/unittest_runner.py

documentation:
	cd docs; doxygen Doxyfile; cd ..


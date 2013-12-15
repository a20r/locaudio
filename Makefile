
all: run_tests

run_tests:
	python tests/unittest_runner.py

depend:
	pip install -r requirements.txt

documentation:
	cd docs; doxygen Doxyfile; cd ..


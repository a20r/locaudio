
all: run_tests

run_tests:
	python tests/unittest_runner.py

depend:
	pip install -r requirements.txt
	mkdir resources
	cd resources; git clone https://github.com/originell/jpype.git; cd ..;
	cd resources/jpype; sudo python setup.py install; cd ..;
	cd resources; git clone https://code.google.com/p/musicg/; cd ..;
	cd resources/musicg/; javac com/musicg/fingerprint/FingerprintSimilarityComputer.java -d ../../; cd ..
	sudo brew install rethinkdb
	mkdir database

documentation:
	cd docs; doxygen Doxyfile; cd ..


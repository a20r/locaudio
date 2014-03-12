
all: run_tests

run_tests:
	python tests/unittest_runner.py

depend:
	sudo brew install rethinkdb
	pip install -r docs/requirements.txt
	mkdir resources
	cd resources; git clone https://github.com/originell/jpype.git; cd ..;
	cd resources/jpype; sudo python setup.py install; cd ..;
	cd resources; git clone https://code.google.com/p/musicg/; cd ..;
	cd resources/musicg/; javac com/musicg/fingerprint/FingerprintSimilarityComputer.java -d ../../; cd ..
	mkdir database
	mkdir imgs
	mkdir sounds

paper:
	cd docs/paper; pdflatex paper.tex; pdflatex paper.tex; pdflatex paper.tex cd ../../;

documentation:
	cd docs; doxygen Doxyfile; cd ..


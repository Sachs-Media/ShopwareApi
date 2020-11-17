localinstall:
	python3 setup.py build
	python3 setup.py bdist_wheel
	python3 setup.py install

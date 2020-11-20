
install-docs:
	pip3 install -r docs/requirements.txt

install-dev-docs:
	pip3 install -r docs/requirements_dev.txt

build-docs:
	cd docs; make build html

build-dev-docs:
	cd docs; make livehtml

test:
	python3 -m unittest

coverage:
	coverage -m unittest
	coverage report
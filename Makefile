
install-docs:
	pip3 install -r docs/requirements.txt

dev-install-docs:
	pip3 install -r docs/requirements_dev.txt

build-docs:
	cd docs; make build html

dev-build-docs:
	cd docs; make livehtml

test:
	python3 -m unittest

coverage:
	coverage -m unittest
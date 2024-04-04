.PHONY: install-all test clean

# Install all dependencies
install-all:
	pip install -r requirements.txt

# Run tests
test:
	python -m unittest discover

# Clean up
clear:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

install-package:
	@read -p "Enter package name: " package; \
	pip install $$package && pip freeze > requirements.txt

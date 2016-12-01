lint:
	tox -e lint

format:
	tox -e format

check-format: format
	git diff --exit-code

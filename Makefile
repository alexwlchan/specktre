lint:
	tox -e lint

format:
	tox -e format

check-format: format
	git diff --exit-code

check-py27:
	tox -e py27

check-py35:
	tox -e py35

check-py36:
	tox -e py36

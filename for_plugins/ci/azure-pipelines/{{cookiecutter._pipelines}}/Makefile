check-required-files:
	(cd .. && python azure-pipelines/scripts/requirements_check.py)

install-base:
	(cd .. && pip install -r src/requirements.txt)

install-test:
	(cd .. && pip install -r src/requirements-test.txt)

lint-with-flake8:
	(cd .. && flake8 --count || true)

lint-with-black:
	(cd .. && black .)

lint-with-isort:
	(cd .. && isort .)

check:
	(cd .. && pytest src/tests)
install:
	cd src/ && pip install -e .

remove:
	pip uninstall python3_capsolver -y

refactor:
	black docs/
	isort docs/

	cd src/ && \
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				python3_capsolver/ tests/ && \
	black python3_capsolver/ tests/ && \
	isort python3_capsolver/ tests/

lint:
	cd src/ && \
	autoflake --in-place --recursive python3_capsolver/ --check && \
	black python3_capsolver/ --check && \
	isort python3_capsolver/ --check-only

upload:
	pip install twine
	cd src/ && python setup.py upload

tests: install
	coverage run --rcfile=.coveragerc -m pytest --verbose --showlocals --pastebin=all tests --disable-warnings && \
	coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	coverage html --precision=3 --skip-empty -d coverage/html/ && \
	coverage xml -o coverage/coverage.xml

doc: install
	cd docs/ && \
	make html -e

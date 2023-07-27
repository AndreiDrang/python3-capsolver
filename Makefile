install:
	cd src/ && pip install -e .

remove:
	pip uninstall python3_capsolver -y

refactor:
	black docs/
	isort docs/

	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				src/ tests/
	black src/ tests/
	isort src/ tests/

lint:
	autoflake --in-place --recursive src/ --check
	black src/ --check
	isort src/ --check-only

upload:
	pip install twine
	cd src/ && python setup.py upload

tests: install
	coverage run --rcfile=.coveragerc -m pytest -vv --showlocals --pastebin=all \
	tests && \
	coverage report --precision=3 --sort=cover --skip-empty --show-missing && \
	coverage html --precision=3 --skip-empty -d coverage/html/ && \
	coverage xml -o coverage/coverage.xml

doc: install
	cd docs/ && \
	make html -e

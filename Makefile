install:
	cd src/ && pip install setup.py

refactor:
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				src/
	black src/
	isort src/

lint:
	autoflake --in-place --recursive src/ --check
	black src/ --check
	isort src/ --check-only

upload:
	pip install twine
	cd src/ && python setup.py upload

tests:
	cd src/ && \
	coverage run --rcfile=.coveragerc -m pytest -s tests -vv --disable-warnings && \
	coverage report --precision=3 --sort=cover -m

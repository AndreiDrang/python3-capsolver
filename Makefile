install:
	cd src/ && pip install -e .

refactor:
	cd src/ && \
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				python3_captchaai/ && \
	black python3_captchaai/ && \
	isort python3_captchaai/

lint:
	cd src/ && \
	autoflake --in-place --recursive python3_captchaai/ --check && \
	black python3_captchaai/ --check && \
	isort python3_captchaai/ --check-only

upload:
	pip install twine
	cd src/ && python setup.py upload

tests:
	cd src/ && \
	coverage run --rcfile=.coveragerc -m pytest -s tests -vv --disable-warnings && \
	coverage report --precision=3 --sort=cover -m

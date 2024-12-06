.PHONY: prepare-env rm-env create-package upload-package

create-env:
	python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

rm-env:
	rm -r .venv/

create-package:
	python setup.py sdist bdist_wheel

upload-package:
	twine upload dist/*


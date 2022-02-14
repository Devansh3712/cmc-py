PY = venv\Scripts\python
PIP = venv\Scripts\pip

clean:
	$(PY) -m pyclean .

format:
	$(PY) -m black ./cmc ./tests

install:
	$(PIP) install poetry pyclean >> NUL 2>&1
	$(PY) -m poetry install

lint:
	$(PY) -m mypy ./cmc

requirements:
	$(PY) -m poetry export -f requirements.txt --output requirements.txt --without-hashes

test:
	$(PY) -m pytest -v

.PHONY: clean format install lint requirements test

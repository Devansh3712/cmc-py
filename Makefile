PY = venv\Scripts\python
PIP = venv\Scripts\pip

clean:
	$(PY) -m pyclean .

dev:
	$(PY) -m uvicorn api.main:app --reload

format:
	$(PY) -m black .

install:
	$(PIP) install poetry pyclean >> NUL 2>&1
	$(PY) -m poetry install

lint:
	$(PY) -m mypy .

requirements:
	$(PY) -m poetry export -f requirements.txt --output requirements.txt --without-hashes

test:
	$(PY) -m pytest -v

.PHONY: clean dev format install lint requirements test

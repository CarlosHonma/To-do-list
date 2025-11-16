VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: venv install run test clean

venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r todo_app/requirements.txt

run: install
	$(PYTHON) run_todo_app.py

test: install
	# run smoke tests
	$(PYTHON) -c "import src.gui, src.utils.database; print('smoke ok')"

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -exec rm -rf {} +

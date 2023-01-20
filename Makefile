SHELL=/bin/bash
VENV = .venv
VENV_BIN = $(VENV)/bin

.venv: 
		python -m venv $(VENV)
		$(VENV_BIN)/python -m pip install --upgrade pip
		$(VENV_BIN)/pip install -r requirements.txt

fmt: format

format: .venv
		$(VENV_BIN)/black .

clean: 
		@rm -rf .venv

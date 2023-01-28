SHELL=/bin/bash
VENV = .venv
VENV_BIN = $(VENV)/bin

.PHONY: .venv
.venv: 
	python -m venv $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt

.PHONY: fmt
fmt:
	$(VENV_BIN)/black .
	$(VENV_BIN)/ruff .

.PHONY: clean
clean: 
	@rm -rf .venv
	@rm -rf ./modules/pytest_cache/
	@rm -rf .ruff_cache/

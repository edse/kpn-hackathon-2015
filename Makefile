PYTHON=`. venv/bin/activate; which python`
PIP=`. venv/bin/activate; which pip`
DEPS:=src/requirements.txt

install:
	@echo 'Installing...'
	$(PIP) install -r $(DEPS)
	@echo 'Done!'

go:
	@echo 'Starting server...'
	$(PYTHON) src/queen.py
	@echo 'Done!'

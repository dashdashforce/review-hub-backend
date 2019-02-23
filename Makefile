init:
	python3 -m venv ./venv
	./venv/bin/pip install --upgrade pip

install-dev:
	./venv/bin/pip install -r ./requirements/dev.txt

run:
	./venv/bin/python run.py
.PHONY: install format lint mypy clean

install:
	poetry run python -m pip install --upgrade pip
	poetry install

format:
	poetry run black .\src\

lint:
	poetry run flake8 --max-line-length 88 --ignore=E203,E231,E402,E501,F401,W503

mypy:
	poetry run mypy .\src\

clean:
	poetry run rm -r __pycache__*
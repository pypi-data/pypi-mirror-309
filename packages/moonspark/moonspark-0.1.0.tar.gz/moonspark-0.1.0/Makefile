install:
	uv pip install -e .

build:
	uv build

lint:
	uvx isort src/moonspark/*.py
	uvx black src/moonspark/*.py
	uvx ruff check src/moonspark/*.py

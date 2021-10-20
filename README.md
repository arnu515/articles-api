# Starter articles API

This API is a starter repository that has a basic articles API complete with authentication. It is written in Python, uses the Flask webframework and Prisma ORM.

## Quickstart

- Requires Python 3.9 and Pip/poetry.

1. Clone the repo
2. Install packages with:
```shell
poetry install # recommended

pip install -r requirements.txt # if you don't have poetry
```
3. Clone `.env.example` to `.env` and fill in the necessary variables
4. Run the app with:
```
poetry run python3 main.py
# OR
python3 main.py
```
5. Visit <http://localhost:5000>
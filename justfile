set windows-shell := ["pwsh.exe", "-c"]
set dotenv-filename := ".env"

install:
    poetry install --sync

run-be:
    poetry run python -m random_coffee_be

#run-fe:
#    poetry run python -m random_coffee_fe

fmt:
    poetry run ruff format random_coffee_be/
#    poetry run ruff format random_coffee_fe/

ruff:
    poetry run ruff check --fix random_coffee_be
#    poetry run ruff check --fix random_coffee_fe

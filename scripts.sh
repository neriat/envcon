#!/bin/bash

function deploy() {
  poetry install && poetry build && poetry publish
}

function increment_minor() {
  poetry version minor && git commit -am "Increment minor version"
}

function fmt() {
  poetry run black .
}

function lint() {
  poetry run flake8 .
}

function mypy() {
  poetry run python -m mypy envcon
}

function mypy_all() {
  poetry run python -m mypy envcon tests \
    --show-error-codes \
    --disallow-untyped-calls \
    --disallow-untyped-defs \
    --disallow-incomplete-defs \
    --disallow-untyped-decorators
}

"$@"

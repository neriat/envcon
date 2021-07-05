import os


def poetry_run(cmd: str):
    os.system(f"poetry run {cmd}")


def deploy():
    os.system("poetry install && poetry build && poetry publish")


def increment_minor():
    os.system('poetry version minor && git commit -am "Increment minor version"')


def black():
    poetry_run("black .")


def flake8():
    poetry_run("flake8 .")


def mypy():
    poetry_run("python -m mypy envcon")


def mypy_all():
    poetry_run(
        "python -m mypy envcon tests"
        " --show-error-codes"
        " --disallow-untyped-calls"
        " --disallow-untyped-defs"
        " --disallow-incomplete-defs"
        " --disallow-untyped-decorators"
    )

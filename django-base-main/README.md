# django-base
A basic boilerplate Django project prepped with poetry and Rollup. It uses the Django project default database SQLite.

## Setup

For history's sake, this setup was based off of the instructions here: https://builtwithdjango.com/blog/basic-django-setup.

1. Install [poetry](https://python-poetry.org/docs/#installation). This allows us to run our project in a virtual environment and will handle the installation of Django and other python libraries.

2. Run `poetry install` to install dependencies.

3. Rename `myproject` to whatever you'd like your project to be named. You will want to change the name in `pyproject.toml`, the Django project directory name `myproject/`, `manage.py`, and `settings.py`.

4. Change `TIME_ZONE` in `settings.py` to your timezone.

5. Run `poetry run python manage.py migrate` to initialize your local database.

6. Create a superuser for your local Django instance. Run `poetry run python manage.py createsuperuser`. Be sure to save your username and password in a responsible location.

7. Install [node](https://nodejs.org/en).

8. Run `npm install`.

9. Run `npm run build`.

## Running the server

Run `poetry run python manage.py runserver`.


## Running other Django commands

See Django documentation for other commands, such as generating and applying migrations. Commands can be used as normal, preceded by `poetry run`. For example, see "Running the server" above.

## Running tests

To run python tests, use `poetry run pytest`.
To run TS/JS tests, use `npm run test`.


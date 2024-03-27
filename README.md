# Solar Events website

Author:
Callum Gavin
mullacy@gmail.com

Supported commands:

## Installing, DB setup and building

```
cd django-base-main
poetry install
poetry run python manage.py migrate

npm install
npm run build
```

## Running the web server

```
poetry run python manage.py runserver
```

Note: you can refresh the page while the GET call to Wikipedia API is in progress to see chart data as it is persisted.

## Run python tests

```
poetry run pytest
```

## Add more solar event data

Append JSON objects to `django-base-main/pages/data/solar_events.json`

## Reset data

```
poetry run python manage.py dbshell
DELETE FROM pages_solarevent;
DELETE FROM pages_revision;
```

# Expected data

```
sqlite> select count(1) from pages_revision;
10115
```

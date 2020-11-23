#!/bin/bash

.PHONY: default
.SILENT:

build:
	docker-compose build

shell:
	docker-compose run --rm web python manage.py shell_plus

migrate:
	docker-compose run --rm web python manage.py migrate --noinput

collectstatic:
	docker-compose run --rm --no-deps web python manage.py collectstatic --noinput

createsuperuser:
	docker-compose run --rm web python manage.py createsuperuser

run:
	docker-compose run --rm --service-ports -e COMMAND=development web

up:
	docker-compose up postgres redis worker web

dependencies:
	docker-compose run --rm --no-deps web pip list --outdated format columns

test:
	docker-compose run --rm web pytest -s -n auto

makemessages:
	docker-compose run --rm --no-deps web python manage.py makemessages -l pt_BR
	docker-compose run --rm --no-deps web python manage.py compilemessages -l pt_BR

coverage:
	docker-compose run --rm web pytest --cov --cov-report term-missing

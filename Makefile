DC = docker compose


.PHONY: up
up:
	${DC} up -d

.PHONY: build
build:
	${DC} up --build -d

.PHONY: logs
logs:
	${DC} logs -f


.PHONY: down
down:
	${DC} down

.PHONY: shell
shell:
	${DC} exec app bash

.PHONY: makemigrations
makemigrations:
	${DC} exec app alembic revision --autogenerate

.PHONY: migrate
migrate:
	${DC} exec app alembic upgrade head
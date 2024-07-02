FROM python:3.12 AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./backend/pyproject.toml ./backend/poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12 AS build-stage

WORKDIR /backend

COPY --from=requirements-stage /tmp/requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ./backend/app /backend/app
COPY ./backend/tests /backend/tests

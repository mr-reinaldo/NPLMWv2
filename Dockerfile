# [Stage 1] Requirements
FROM python:3.12 AS requirements-stage

# Define o diretório de trabalho
WORKDIR /tmp

# Instala o poetry
RUN pip install poetry==1.8.3

# Copia os arquivos de dependências
COPY ./backend/pyproject.toml ./backend/poetry.lock* /tmp/

# Instala as dependências
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# [Stage 2] Build
FROM python:3.12 AS build-stage

# Cria grupo e usuário de sistema sem senha.
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Define o diretório de trabalho
WORKDIR /backend

# Define as variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=${PYTHONPATH}:/backend
ENV PYTHONUNBUFFERED 1

# Copia os arquivos de dependências do stage anterior
COPY --from=requirements-stage /tmp/requirements.txt /backend/requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# Define as permissões do diretório
RUN chown -R appuser:appuser /backend

# Define o usuário padrão
USER appuser

# Copia os arquivos do projeto
COPY ./backend/app /backend/app
COPY ./backend/tests /backend/tests

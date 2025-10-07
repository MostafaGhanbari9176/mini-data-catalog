FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl
# cleans up cache to reduce image size
RUN rm -rf /var/lib/apt/lists/*
# installing poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY . /app/

EXPOSE 8000

COPY docker-entrypoint.sh /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]

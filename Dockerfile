FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "main.py"]

FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root

COPY . .

COPY session_ales.session /app/session_ales.session
COPY session_mandarisha.session /app/session_mandarisha.session

CMD ["poetry", "run", "python", "main.py"]

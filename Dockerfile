FROM python:3.11.2-slim

WORKDIR /app

ENV PYTHONPATH .

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi || echo "Poetry install failed"

EXPOSE ${SERVER_PORT}

COPY . .

CMD ["python", "app/main.py"]

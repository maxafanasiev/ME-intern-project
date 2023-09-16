FROM python:3.11.2-slim

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi || echo "Poetry install failed"

EXPOSE 8000

COPY . .

CMD ["python", "app/main.py"]

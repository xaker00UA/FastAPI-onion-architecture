FROM  python:3.12.7-slim
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install poetry
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi
EXPOSE 8000
COPY . .
FROM python:3.12.8-slim 
WORKDIR /app
RUN pip install poetry 
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main # Установка без зависимостей для разработки
ADD . ./


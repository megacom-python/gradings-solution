FROM python:3-slim
RUN pip install poetry
COPY . .
RUN poetry add psycopg2-binary
RUN poetry install --no-deps 
CMD ["poetry", "show"]
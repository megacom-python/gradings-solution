FROM python:3-slim
WORKDIR /app
RUN apt-get update && apt-get install libpq-dev -y
RUN pip install poetry
COPY . .
RUN poetry add psycopg2-binary
RUN poetry install --no-root
#CMD poetry run python manage.py runserver 0.0.0.0:8000
#ENTRYPOINT ["start.sh"]
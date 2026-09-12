FROM postgres:15

COPY ./database/schema.ddl /docker-entrypoint-initdb.d/schema.sql
COPY ./database/datafiller.sql /docker-entrypoint-initdb.d/datafiller.sql
# FROM python:3.10.21-slim

# COPY ./config_folder .

# RUN pip install flask flask_sqlalchemy psycopg2-binary

# CMD ["python", "main.py"]
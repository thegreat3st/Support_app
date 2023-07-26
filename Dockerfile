FROM python:3.11-slim

WORKDIR /app/

COPY Pipfile Pipfile.lock src/ ./

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install pipenv \
    && pip install watchdog


RUN pipenv sync --dev --system

CMD python manage.py runserver 0.0.0.0:8000
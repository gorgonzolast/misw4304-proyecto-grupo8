FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc-dev libpq-dev

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3000

EXPOSE 3000

CMD ["pipenv", "run", "flask", "run"]

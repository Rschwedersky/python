FROM python:3.9-buster

WORKDIR /app

COPY ./requirements.txt .

# You will need this if you need PostgreSQL, otherwise just skip this
RUN apt-get update && apt-get install libpq-dev gcc python3-dev musl-dev libffi-dev -y
RUN pip install uwsgi
RUN pip install -r requirements.txt

COPY ./src .
ENV PORT=8000
EXPOSE 8000
# Runner script here
CMD ["sh", "/app/runner.sh"]
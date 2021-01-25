FROM python:3.7.4-alpine

COPY app/requirements.txt .

RUN apk update

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

RUN pip install -r requirements.txt

COPY app /app

WORKDIR /app

EXPOSE 5000

ENTRYPOINT [ "./start.sh" ]

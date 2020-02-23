FROM python:3.7.6-alpine as compile-image
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt /requirements.txt
RUN apk add bash gcc musl-dev libffi-dev postgresql-dev make libxslt-dev jpeg-dev && pip install --upgrade pip && python -m venv /opt/venv && pip install -r requirements.txt

FROM python:3.7.6-alpine as build-image
RUN adduser -D -u 1002 -s /bin/bash bookie && mkdir /home/bookie/project
COPY --from=compile-image /opt/venv /home/bookie/.local
USER bookie
WORKDIR /home/bookie/project
COPY --chown=bookie . /home/bookie/project/
ENV PATH="/home/bookie/.local/bin:$PATH"
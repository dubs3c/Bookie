FROM python:3.7.6-alpine
ENV PYTHONUNBUFFERED 1
RUN apk --no-cache add --update                                         \
        --repository http://dl-3.alpinelinux.org/alpine/edge/testing/   \
        dos2unix
RUN apk add bash gcc musl-dev libffi-dev postgresql-dev make libxslt-dev jpeg-dev && adduser -D -u 1002 -s /bin/bash bookie && pip install --upgrade pip
USER bookie
RUN mkdir /home/bookie/project
WORKDIR /home/bookie/project
COPY --chown=bookie . /home/bookie/project/
RUN pip install -r requirements.txt --user && echo "export PATH=$(python -c 'import site; print(site.USER_BASE + "/bin")'):$PATH" >> ~/.bashrc
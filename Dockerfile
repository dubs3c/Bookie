FROM python:3
ENV PYTHONUNBUFFERED 1
RUN useradd -ms /bin/bash bookie
USER bookie
RUN mkdir /home/bookie/project
WORKDIR /home/bookie/project
COPY --chown=bookie . /home/bookie/project/
RUN pip install -r requirements.txt --user
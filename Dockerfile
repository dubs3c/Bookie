FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN useradd -u 1002 -ms /bin/bash bookie && pip install --upgrade pip
USER bookie
RUN mkdir /home/bookie/project
WORKDIR /home/bookie/project
COPY --chown=bookie . /home/bookie/project/
RUN pip install -r requirements.txt --user && echo "export PATH=$(python -c 'import site; print(site.USER_BASE + "/bin")'):$PATH" >> ~/.bashrc
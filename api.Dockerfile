FROM python:3.7.3-slim

RUN mkdir /project
WORKDIR /project
COPY requirements.txt /project/

RUN apt-get update \
    && apt-get install -y build-essential python-dev \
    && pip install -r requirements.txt \
    && apt-get purge -y build-essential python-dev \
    && apt-get autoremove -y \
    && apt-get clean

COPY . /project/

ENTRYPOINT ["uwsgi", "uwsgi.ini"]
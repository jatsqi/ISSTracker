FROM python:3.8.5-alpine

# Environment
ENV REDISHOST="localhost"
ENV REDISPW="password"

# Init
WORKDIR /usr/src/app
COPY . .
RUN rm dump.rdb

# Setup
RUN apt-get install libxml2-dev libxslt-dev python-dev
RUN pip install -r requirements.txt

# Finalize
ENTRYPOINT python tewst
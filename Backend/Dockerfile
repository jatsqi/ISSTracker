FROM python:3.8.5

# Environment
ENV REDISHOST="localhost"
ENV REDISPW="password"

# Init
WORKDIR /usr/src/app
COPY . .
RUN rm dump.rdb

# Setup
RUN apk update && apk add --no-cache libxml2-dev libxslt-dev
RUN pip install -r requirements.txt

# Finalize
ENTRYPOINT python tewst
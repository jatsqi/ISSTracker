FROM python:3.8.5-alpine

# Environment
ENV FLASK_APP = application.py

# Init
WORKDIR /usr/src/app
COPY . .

# Setup
RUN pip install -r requirements.txt

# Finalize
ENTRYPOINT [ "flask run" ]
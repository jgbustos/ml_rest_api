# This is an official Python runtime, used as the parent image
# Python 3.6 on Debian "Buster"
FROM python:3.6-slim-buster

# Parent image to run uder Nginx+uWSGI
# Python 3.6 on Debian "Stretch"
# FROM tiangolo/uwsgi-nginx-flask:python3.6

LABEL maintainer="j.garciadebustos@godeltech.com"

COPY requirements.txt /app/

RUN pip install --upgrade pip \
 && pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

# Uncomment to set listen port for Nginx+uWSGI
# ENV LISTEN_PORT 8888  

EXPOSE 8888
ENV PYTHONPATH "${PYTHONPATH}:/app/ml_rest_api"

# Comment the two lines below to run under Nginx+uWSGI
ENTRYPOINT ["python3"]
CMD ["ml_rest_api/app.py"]

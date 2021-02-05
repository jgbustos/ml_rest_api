# This is an official Python runtime, used as the parent image
# Python 3.8 on Debian "Buster"
FROM python:3.8-slim-buster

# Parent image to run under Nginx+uWSGI
# Python 3.8 on Debian "Stretch"
# FROM tiangolo/uwsgi-nginx-flask:python3.8

# Parent image to run under Meinheld+Gunicorn
# Python 3.8 on Debian "Stretch"
# FROM tiangolo/meinheld-gunicorn-flask:python3.8

LABEL maintainer="j.garciadebustos@godeltech.com"

COPY requirements.txt /app/

RUN pip install --upgrade pip \
 && pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

# Uncomment to set listen port for Nginx+uWSGI
# ENV LISTEN_PORT 8888

# Uncomment to set listen port for Meinheld+Gunicorn
# ENV PORT 8888
# ENV BIND 0.0.0.0:8888

EXPOSE 8888
ENV PYTHONPATH "${PYTHONPATH}:/app/ml_rest_api"

# Comment the two lines below to run under Nginx+uWSGI
ENTRYPOINT ["python3"]
CMD ["ml_rest_api/app.py"]

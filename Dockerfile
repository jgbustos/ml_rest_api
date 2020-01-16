# This is an official Python runtime, used as the parent image
# Python 3.6 on Debian "Buster"
FROM python:3.6-slim-buster

LABEL maintainer="j.garciadebustos@godeltech.com"

COPY requirements.txt /app/

RUN pip install --upgrade pip \
 && pip install -r app/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8888

ENV PYTHONPATH "${PYTHONPATH}:/app/ml_rest_api"

ENTRYPOINT ["python3"]

CMD ["ml_rest_api/app.py"]

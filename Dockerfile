# This is an official Python runtime, used as the parent image
# Python 3.6 on Debian "Buster"
FROM python:3.6-slim-buster

LABEL maintainer="j.garciadebustos@godeltech.com"

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

EXPOSE 8888

ENTRYPOINT ["python3"]

CMD ["ml_rest_api/app.py"]

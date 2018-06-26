# this is our own base image
FROM jgbustos/ml-model-base:latest

LABEL maintainer="j.garciadebustos@godeltech.com"

COPY . /app
WORKDIR /app

EXPOSE 8888

ENTRYPOINT ["python3"]

CMD ["ml_rest_api/app.py"]

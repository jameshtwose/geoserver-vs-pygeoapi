FROM ubuntu:22.04

ENV TZ=Europe/Amsterdam \
    DEBIAN_FRONTEND=noninteractive

ENV PYGEOAPI_CONFIG=pygeoapi-config.yaml
ENV PYGEOAPI_OPENAPI=openapi-config.yaml

RUN env

RUN apt update \
    && apt -y install python3.10 python3-pip postgresql-client libpq-dev

WORKDIR /usr/src

COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /usr/app

WORKDIR /usr/app

EXPOSE 5001

CMD ["python3.10", "main.py"]
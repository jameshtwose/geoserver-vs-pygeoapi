FROM ubuntu:22.04

ENV TZ=Europe/Amsterdam \
    DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt -y install openjdk-17-jdk openjdk-17-jre maven unzip wget

WORKDIR /usr/share

RUN wget https://build.geoserver.org/geoserver/2.25.x/geoserver-2.25.x-latest-bin.zip \
    && mkdir /usr/share/geoserver \
    && mv geoserver-2.25.x-latest-bin.zip /usr/share/geoserver

WORKDIR /usr/share/geoserver/

RUN unzip geoserver-2.25.x-latest-bin.zip \
    && rm geoserver-2.25.x-latest-bin.zip

RUN rm /usr/share/geoserver/webapps/geoserver/WEB-INF/web.xml

COPY custom_web.xml /usr/share/geoserver/webapps/geoserver/WEB-INF/web.xml

WORKDIR /usr/share/geoserver/bin

ENV GEOSERVER_HOME=/usr/share/geoserver

EXPOSE 8080

RUN echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile

CMD ["./startup.sh"]
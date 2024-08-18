FROM ubuntu:22.04
 
ENV TZ=Europe/Amsterdam \
    DEBIAN_FRONTEND=noninteractive
 
RUN apt-get update \
    && apt-get -y install python3.10 python3-pip

COPY . /usr/app
WORKDIR /usr/app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8081

CMD ["streamlit", "run", "dashboard.py", "--server.port=8081", "--browser.gatherUsageStats=False"]
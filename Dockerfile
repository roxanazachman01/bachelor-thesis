FROM jenkins/agent:jdk11

USER root

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y build-essential
RUN apt install -y libffi-dev 
RUN apt install -y libssl-dev

WORKDIR /usr/src/app
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER jenkins
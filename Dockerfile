FROM ubuntu:20.04

ENV TZ=America/Asuncion DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils nano git
RUN apt-get -y install python3.9 libapache2-mod-wsgi-py3
RUN ln /usr/bin/python3.9 /usr/bin/python
RUN apt-get -y install python3-pip
RUN ln -sf /usr/bin/pip3 /usr/bin/pip
RUN pip install --upgrade pip
COPY . .
ENV PYTHONUNBUFFERED 1
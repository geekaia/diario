FROM ubuntu
# File Author / Jacinto Jose Franco

RUN apt-get update
RUN apt-get install -y --force-yes mysql-server 

EXPOSE 80
EXPOSE 8000

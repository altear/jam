FROM python:3.6.8-stretch

WORKDIR ~

RUN apt-get update 
RUN apt-get upgrade -y 
RUN apt-get install -y git

RUN pip install Django==2.2
RUN git clone https://github.com/altear/jam.git
RUN ls
CMD python jam/jam_app/manage.py runserver 


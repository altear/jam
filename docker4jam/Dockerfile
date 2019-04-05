FROM python:3.6.8-alpine

WORKDIR ~

RUN pip install Django==2.2
RUN git clone https://github.com/altear/jam.git

CMD python jam/jam_app/manage.py runserver 


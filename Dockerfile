FROM python:3
# Autor
MAINTAINER Antonio Alcalá Martínez

RUN apt-get update
RUN apt-get install -y python-celery
RUN apt-get install -y python3-celery
RUN apt-get install -y build-essential tcl
RUN wget http://download.redis.io/redis-stable.tar.gz
RUN tar xzvf redis-stable.tar.gz
RUN cd redis-stable && make
RUN cd redis-stable && make test
RUN cd redis-stable && make install
RUN mkdir etc/redis
COPY . .
RUN cp install_server.sh redis-stable/utils/install_server.sh


# Instalación de git y clonado del proyecto



# Instalación de las dependecncias del proyecto

RUN pip3 install -r requirements.txt

RUN wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | apt-key add -
RUN apt-get install -y rabbitmq-server
EXPOSE 80

CMD ./redis-stable/utils/install_server.sh && service rabbitmq-server start && python3 manage.py migrate &&export C_FORCE_ROOT="true" &&  (celery -A BuscadorBDMedical worker -l info &) &&   python3 manage.py runserver 0.0.0.0:80

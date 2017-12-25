FROM python:3
# Autor
MAINTAINER Antonio Alcalá Martínez

RUN apt-get update
RUN apt-get install -y python-celery
RUN apt-get install -y python3-celery
RUN apt-get install -y build-essential tcl
RUN wget http://download.redis.io/redis-stable.tar.gz
RUN tar xzf redis-stable.tar.gz
RUN cd redis-stable && make
RUN cd redis-stable && make test
RUN cd redis-stable && make install
RUN mkdir etc/redis
COPY . .
RUN ./redis-stable/utils/install_server.sh
RUN cp conf_redis/6379.conf etc/redis/
RUN touch var/lib/redis/6379
RUN touch var/log/redis_6379.log
# Instalación de git y clonado del proyecto



# Instalación de las dependecncias del proyecto

RUN pip3 install -r requirements.txt

RUN wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | apt-key add -
RUN apt-get install -y rabbitmq-server
CMD ./usr/local/bin/redis-server && ./usr/local/bin/redis.cli && cp /tmp/6379.conf /etc/init.d/redis_6379 && chmod +x /etc/init.d/redis_6379
CMD  python3 manage.py migrate &&  (update-rc.d redis_6379 defaults &) && (/etc/init.d/redis_6379 start &)  && service rabbitmq-server start && (python3 manage.py runserver 0.0.0.0:80 &) && export C_FORCE_ROOT="true"  &&  celery -A BuscadorBDMedical worker -l info
EXPOSE 80 21

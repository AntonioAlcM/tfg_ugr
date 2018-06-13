FROM python:3
# Autor
MAINTAINER Antonio Alcalá Martínez

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python-celery
RUN apt-get install -y python3-celery
RUN apt-get install -y build-essential tcl
RUN pip install -U pip
RUN pip3 install -U pip
RUN wget http://download.redis.io/redis-stable.tar.gz
RUN tar xzvf redis-stable.tar.gz
RUN cd redis-stable && make
RUN make distclean -C ./redis-stable
RUN make -C ./redis-stable
RUN make install -C ./redis-stable
RUN mkdir etc/redis
RUN ./redis-stable/utils/install_server.sh
COPY . .
COPY ./conf_redis/6379.conf /etc/redis


# Instalación de las dependecncias del proyecto

RUN pip3 install -r requirements.txt


EXPOSE 80
CMD python3 manage.py migrate && python3 manage.py collectstatic --noinput && (update-rc.d redis_6379 defaults &)  && (/etc/init.d/redis_6379 start  &) && (python3 manage.py runserver 0.0.0.0:80 &) && export C_FORCE_ROOT="true"  &&  celery -A BuscadorBDMedical worker -l info

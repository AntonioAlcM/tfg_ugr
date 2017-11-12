FROM ubuntu:16.04
# Autor
MAINTAINER Antonio Alcalá Martínez

# Actualización de los repositorios e instalacion de python
RUN apt-get update
RUN apt-get install -y python-setuptools
RUN apt-get install -y python-dev
RUN apt-get install -y build-essential
RUN apt-get install -y libpq-dev
RUN apt-get install -y python-pip
RUN pip install --upgrade pip

# Instalación de git y clonado del proyecto
RUN apt-get install -y git
RUN git clone https://github.com/AntonioAlcM/tfg_ugr.git

# Instalación de las dependecncias del proyecto
RUN cd tfg_ugr
RUN ls -l
RUN pip install -r requirements.txt
RUN python manage.py test

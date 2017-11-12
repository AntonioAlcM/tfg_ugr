FROM ubuntu:16.04
# Autor
MAINTAINER Antonio Alcalá Martínez

# Actualización de los repositorios e instalacion de python
RUN apt-get update
RUN sudo apt-get -y install python-dev
RUN sudo apt-get install -y python-setuptools
RUN sudo apt-get install -y build-essential
RUN sudo apt-get -y install libpq-dev
RUN sudo easy_install pip
RUN sudo pip install --upgrade pip

# Instalación de git y clonado del proyecto
RUN apt-get install -y git
RUN git@github.com:AntonioAlcM/tfg_ugr.git

# Instalación de las dependecncias del proyecto
RUN cd tfg_ugr
RUN pip install -r requeriments.txt

FROM ubuntu:16.04
# Autor
MAINTAINER Antonio Alcalá Martínez

# Actualización de los repositorios e instalacion de python
RUN apt-get update
RUN apt-get install -U python-setuptools
RUN apt-get install -U python-dev
RUN apt-get install -U build-essential
RUN apt-get install -U libpq-dev
RUN apt-get install -U python-pip
RUN pip install --upgrade
RUN apt-get install net-tools

# Instalación de git y clonado del proyecto
RUN apt-get install -y git
RUN git clone https://github.com/AntonioAlcM/tfg_ugr.git
# Instalación de las dependecncias del proyecto
RUN pip install -r tfg_ugr/requirements.txt
EXPOSE 8000
CMD cd tfg_ugr && gunicorn BuscadorBDMedical.wsgi --log-file - --bind 0.0.0.0:8000

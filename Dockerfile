FROM python:3
# Autor
MAINTAINER Antonio Alcalá Martínez

# Actualización de los repositorios e instalacion de python
RUN apt-get install net-tools

# Instalación de git y clonado del proyecto
COPY . .
# Instalación de las dependecncias del proyecto
RUN pip install -r requirements.txt
EXPOSE 80
CMD gunicorn BuscadorBDMedical.wsgi --log-file - --bind 0.0.0.0:80

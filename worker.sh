#!/bin/bash
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery --workdir . -Ofair' &
gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery -c 4 --workdir . -n worker0' &
gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery -c 4 --workdir . -n worker1' &
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery -c 2 --workdir . -n worker2' &
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery -c 2 --workdir . -n worker3' &
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery -c 1 --workdir . -n worker4' &
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery -c 1 --workdir . -n worker5' &
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery -c 1 --workdir . -n worker6' &
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery -c 1 --workdir . -n worker7' &
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery --workdir . -n worker8' &
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery --workdir . -n worker9' &
#gnome-terminal -e 'celery  worker -A BuscadorBDMedical -Q celery --workdir . -n worker10' &

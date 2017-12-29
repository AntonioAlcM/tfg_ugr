from fabric.api import *
def instalar_dependencias_django():
	run('cd /vagrant && sudo  pip3 install -r requirements.txt')
def instalar_dependencias_backend():
	run('cd /vagrant/backend && sudo pip3 install -r requirements.txt')
def test_django():
	run('nohup sudo -E  celery /vagrant/worker -A BuscadorBDMedical -Q celery' , pty=False)
	run('nohup sudo -E  python3 /vagrant/backend/test_tratamientoDatos.py ', pty=False)
	run('nohup sudo -E  python3 /vagrant/manage.py test', pty=False)
def test_backend():
	run('nohup sudo -E celery worker -A /vagrant/backend/celeryconfig -Q celery' , pty=False)
	run('nohup sudo -E  python3 /vagrant/backend/test_tratamientoDatos.py ', pty=False)
@parallel
def ejecutar_django():
	run('python3 /vagrant/manage.py migrate')
	sudo(' screen -d -m python3 /vagrant/manage.py runserver 0.0.0.0:80 ', pty=False)
	run(' screen -d -m celery  worker -A BuscadorBDMedical -Q celery --workdir /vagrant/ -l info ', pty=False)

def ejecutar_backend():
	sudo('screen -d -m python3 /vagrant/backend/tratamientoDatos.py', pty=False)
	run('screen -d -m celery  worker -A celeryconfig -Q celery --workdir /vagrant/backend/ -l info', pty=False)


def ejecutar_redis_rabbit():
	sudo(' service rabbitmq-server start')
	sudo('  nohup sudo -E  service redis start ', pty=False)

def reiniciar_redis_rabbit():
	sudo(' service rabbitmq-server restart')
	sudo(' screen -d -m  service redis restart' , pty=False)

def parar_redis_rabbit():
	run(' systemctl stop redis_379')
	run(' service rabbitmq-server stop')

def parar():
	sudo('pkill python3')

from fabric.api import *
def instalar_dependencias_django():
	run('cd /vagrant && sudo  pip3 install -Ur requirements.txt')
def instalar_dependencias_backend():
	run('cd /vagrant/backend && sudo pip3 install -Ur requirements.txt')
def test_django():
	run('celery  worker -A BuscadorBDMedical -Q celery -D --workdir /vagrant/ ', pty=False)
	run('nohup sudo -E  python3 /vagrant/manage.py test', pty=False)
def test_backend():
	run('celery  worker -A celeryconfig -D -Q celery --workdir /vagrant/backend/' , pty=False)
	run('python3 /vagrant/backend/test_TratamientoDatos.py ', pty=False)

def ejecutar_django():
	run('python3 /vagrant/manage.py migrate')
	run('celery  worker -A BuscadorBDMedical -Q celery -D --workdir /vagrant/ ', pty=False)
	sudo(' screen -d -m python3 /vagrant/manage.py runserver 0.0.0.0:80 ', pty=False)


def ejecutar_backend():
	run('celery  worker -A celeryconfig -D -Q celery --workdir /vagrant/backend/', pty=False)
	sudo('screen -d -m python3 /vagrant/backend/tratamientoDatos.py', pty=False)



def ejecutar_redis_rabbit():
	sudo(' service rabbitmq-server start')
	sudo(' nohup sudo -E  update-rc.d redis_6379 defaults', pty=False)
	sudo('pkill redis')
	sudo('screen -d -m   /etc/init.d/redis_6379 start ', pty=False)
	#redis-server /etc/redis/6379.conf

def reiniciar_redis_rabbit():
	sudo(' service rabbitmq-server restart')
	sudo(' screen -d -m /etc/init.d/redis_6379 restart' , pty=False)

def parar_redis_rabbit():
	run(' systemctl stop redis_379')
	run(' service rabbitmq-server stop')

def parar():
	sudo('pkill python3')

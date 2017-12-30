from fabric.api import *
def instalar_dependencias_django():
	run('cd /vagrant && sudo pip3 install -r requirements.txt')
def instalar_dependencias_backend():
	run('cd /vagrant/backend && sudo pip3 install -r requirements.txt')
def test_django():
    run('cd /vagrant && python3 manage.py test')
def test_backend():
    run('cd /vagrant/backend && python3 test_tratamientoDatos.py')
def ejecutar_django():
	run('cd /vagrant && python3 manage.py migrate')
	sudo('cd /vagrant && python3 manage.py runserver 0.0.0.0:80')
	run('cd /vagrant && python3 celery worker -A BuscadorBDMedical -Q celery')
def ejecutar_backend():
    sudo('cd /vagrant/backend && sudo python3 tratamientoDatos.py')
    run('cd /vagrant/backend && celery worker -A celeryconfig -Q celery')
def ejecutar_redis_rabbit():
	run('sudo service redis start')
	run('sudo service rabbitmq-server start')
def reiniciar_redis_rabbit():
	run('sudo service redis restart')
	run('sudo service rabbitmq-server restart')
def parar_redis_rabbit():
	run('sudo service redis stop')
	run('sudo service rabbitmq-server stop')

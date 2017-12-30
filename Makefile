
desplegar:
	vagrant up --provider=aws
	vagrant ssh-config | grep HostName > dns_publicos.txt
	. ./obtenerDNS.sh
obtener_dns:
	vagrant ssh-config | grep HostName > dns_publicos.txt
	. ./obtenerDNS.sh
desplegar_django:
	vagrant up django --provider=aws
	. ./obtenerDNS.sh
desplegar_backend:
	vagrant up backend --provider=aws
	. ./obtenerDNS.sh
desplegar_bd:
		vagrant up bd --provider=aws
		. ./obtenerDNS.sh
parar_vagrant:
	vagrant halt

install:
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_D) instalar_dependencias_django
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_B) instalar_dependencias_backend
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_R) ejecutar_redis_rabbit
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_B) ejecutar_backend
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_D) test_django
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_B) test_backend
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_D) ejecutar_django

instalar_dependencias:
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_D)instalar_dependencias_django
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_B) instalar_dependencias_backend

test:
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_D) test_django
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_B) test_backend

ejecutar:
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_R) ejecutar_redis_rabbit
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_D) ejecutar_django
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_B) ejecutar_backend

reiniciar_bd:
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_R) reiniciar_redis_rabbit

parar_bd:
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_R) parar_redis_rabbit

provisionar_bd:
	vagrant provision bd
provisionar_django:
	vagrant provision django
provisionar_backend:
	vagrant provision backend
provisionar:
	vagrant provision

destruir_bd:
	vagrant destroy -f bd
destruir_django:
	vagrant destroy -f django
destruir_backend:
	vagrant destroy -f backend
destruir:
	vagrant destroy -f
reiniciar:
	vagrant reload
parar_aplicacion:
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_D) parar
	fab -f ./despliegue/fabfile.py -i ~/.ssh/iv.pem -H ubuntu@$(DNS_B) parar

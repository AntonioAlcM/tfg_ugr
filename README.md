# Buscador de datos médicos  
[![Build Status](https://travis-ci.org/AntonioAlcM/tfg_ugr.svg?branch=master)](https://travis-ci.org/AntonioAlcM/tfg_ugr) [![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]() [![license](https://www.gnu.org/graphics/lgplv3-88x31.png)](https://www.gnu.org/licenses/lgpl.html)

Vamos a desarrollar una aplicación web, que haga una búsqueda múltiple en 3 bases de datos distintas.
Cada búsqueda contendrá, una palabra de búsqueda y un conjunto de filtros.    
Las búsquedas se mostraran en una lista, cuyos campos serán, descripción, base de datos en la que se encontró y enlace al objeto de la base de datos. Las búsquedas tendrán un sistema de filtrado.  

## Servicios y herramientas que se van a usar

Voy a usar una base de datos NoSQL, porque me interesa que sea escalable.  
Voy a usar Python y django para programar la aplicación.
Será desplegada en un servidor web en la nube.

## Testeo

En este proyecto vamos a utilizar la librería unittest, se ha elegido por su amplia gama de funcionalidades.

## Integración continua

Como sistema de integración continua he usado travis-ci, se ha elegido travis-ci por su fácil manejo, ademas permite instalar las dependencias requirements.txt de python de forma automática. Otra ventaja que nos aporta es la posibilidad de ejecutar los test de forma inmediata, cuando se añade nuevas funcionalidades a la clase que se esta testeando.

## Despliegue en PaaS  
Después de observar las distintas opciones Paas (Engine yard, Openshif, Google app engine, Heroku, Appfog, Azure, AWS y Cloudno.de), hemos decidido usar heroku, ya que es la que mas recursos nos ofrece, en su modo gratuito. Hay otras Paas que nos dan mas recursos pero están mas limitadas en el tiempo, nos interesa disponer de mas tiempo para probar las plataformas. Además otra ventaja de Heroku es que permite la integración continua con Travis

### Migración del proyecto de Django a Heroku
Para migrar el proyecto vamos a seguir los pasos de este [tutorial](https://devcenter.heroku.com/articles/django-app-configuration), que podemos encontrar en la documentación de Heroku.
1. Instalamos el gunicorn, sino lo tenemos instalado y lo metemos en el archivo requirements.txt
2. Creamos el archivo Procfile, este archivo se usa para declarar explícitamente los tipos de procesos y puntos de entrada de su aplicación
	El contenido del mismo será: "web: gunicorn BuscadorBDMedical.wsgi --log-file -"


### Creación proyecto Heroku
Hay dos opciones, la primera es creando el proyecto desde la web de Heroku, es un proceso bastante intuitivo y fácil. Y la que voy a explicar es usando los comandos del toolbelt que nos proporciona Heroku.
1. Primero nos logueamos
![imagen](https://github.com/AntonioAlcM/IV17-18-Autoevaluacion/blob/master/Tema3/Imagenes/ejercicio2.1.png?raw=true)
2. Creamos el proyecto en Heroku con el comando "heroku create buscadorbdmedical"  
![imagen](https://github.com/AntonioAlcM/IV17-18-Autoevaluacion/blob/master/Tema3/Imagenes/hito3.1.png?raw=true)
4. Deshabilitamos por ahora la configuración de los archivos estáticos "heroku config:set DISABLE_COLLECTSTATIC=0"  
5. Hacemos un git push heroku master para hacer el despliegue
![imagen](https://github.com/AntonioAlcM/IV17-18-Autoevaluacion/blob/master/Tema3/Imagenes/hito3.2.png?raw=true)
Para asegurar la versión de python que queremos ejecutar, deberemos crear un archivo llamado runtime.txt en el directorio raíz de nuestro proyecto, dicho archivo contendrá la versión de python que queremos ejecutar. No es obligatorio su inclusión, pero en nuestro caso como queremos que se ejecute en la versión 2.7 de python lo añadiremos.

### Despliegue desde Github de forma automática
Para desplegar la aplicación en github de forma automática y que además pase los test haremos:
1. Nos vamos a la pagina web de Heroku en personal apps seleccionamos la aplicación.
2. Nos vamos al menú Deploy.
3. En Deployment method seleccionamos GitHub, buscamos el nombre del repositorio y lo seleccionamos.
4. Activamos la opción Automatically deploys from, por defecto activara la versión de la rama maestra.
5. Activamos Wait for CI to pass before deploy.
Con estos pasos ya tenemos desplegada nuestra aplicación. Para desplegar la aplicación en github nos hemos basado en [este manual](https://devcenter.heroku.com/articles/github-integration).
![imagen](https://github.com/AntonioAlcM/IV17-18-Autoevaluacion/blob/master/Tema3/Imagenes/hito3.3.png?raw=true)

### Observaciones
Es importante configurar el archivo settings para poder desplegar correctamente la aplicación. Para ello vamos a seguir la [guía](https://devcenter.heroku.com/articles/django-app-configuration) de Heroku.
Hay tres direcciones dentro de la aplicación web:
1. Probar el JSON status  
Despliegue https://buscadorbdmedical.herokuapp.com/status
2. Probar el JSON status mas el campo ejemplo  
[Enlace a la página ejemplo](https://buscadorbdmedical.herokuapp.com/buscador/ejemplo/)
3. Probar la aplicación REST  
[Enlace a la página para probar REST](https://buscadorbdmedical.herokuapp.com/buscador/rest/)

## Despliegue en DockerHub y Zeit  
Para poder crear un contenedor de Docker de forma automática, lo primero que debemos hacer es crear un Dockerfile en el directorio raíz de nuestro repositorio y configurarlo utilizando los comandos  que viene explicados en la documentación. En dicho Dockerfile elegiremos la imagen de sistema operativo que queremos instalar en el contenedor, los comandos que deseamos ejecutar una vez instalado el sistema operativo, además de descargar nuestro repositorio en el contendedor. En mi caso añadiré una línea en el Dockerfile, para que despliegue la aplicación

### Despliegue en DockerHub
Para almacenar en DockerHub el contenedor que hemos definido en nuestro repositorio de github, lo que debemos hacer es irnos al menú create y elegimos la opción create automated build, seleccionamos github y le pasamos el repositorio que tiene el Dockerfile.
![imagen](https://github.com/AntonioAlcM/IV17-18-Autoevaluacion/blob/master/Tema4/Imagenes/docker0.0.png?raw=true)  
Para descargar el contenedor en nuestra máquina tenemos dos opciones:
1. docker pull antonioalcm/tfg_ugr
2. sudo docker build -t buscadorbdmedical

[Enlace a DockerHub](https://hub.docker.com/r/antonioalcm/tfg_ugr/)

### Despliegue en Zeit
Para desplegar el contenedor de Docker en Zeit, debemos instalar now, para ellos usaremos npm install now -g, una vez instalado nos vamos a la carpeta donde esta el archivo Dockerfile y ejecutamos:

	sudo now --public

Con este comando nos empezará a desplegar el contenedor en Zeit

Contenedor: https://antonio-fxtswcikye.now.sh/
### Despliegue en Zeit a través de travis-cli
Para desplegar tu contenedor Docker a través de travis, lo primero que debes hacer es crear un archivo package.json, debes configurar el archivo con las siguientes líneas, estas son las líneas mínimas obligatorias:

	"scripts": {
		"clean": "now rm -y Antonio " ,
		"start": "now -e NODE_ENV=production --token $NOW_TOKEN --docker --static 		--public",
		"alias": "now alias --token $NOW_TOKEN"
	}

Una vez configurado el package.json, vamos a configurar el archivo .travis.yml, lo configuraremos para que travis lance el comando now y despliegue de forma automática el contenedor para ello configuraremos travis de la siguiente forma

	before_script: npm install now -g, npm run clean
	after_script: npm run alias
	script:
	- npm run start
	- etc...
### Despliegue en AWS

#### Configuración de red y obtención de credenciales

1. Obtención de credenciales para poder conectarnos a aws    
	* Primero deberemos crear un usuario en el apartado My security Credentials del menú de usuario  
	*	Una vez creado dicho usuario deberemos pinchar en el submenú Policies, pinchando sobre AdministratorAccess, luego seleccionaremos la pestaña Attached entities, pulsando sobre el botón Attach y seleccionando el usuario recién creado.  
	* El siguiente paso es  crear las credenciales de seguridad, para ello volveremos al menú de Users, en dicho menu pincharemos sobre el nombre del usuario. Nos aparecerá una nueva ventana, donde pincharemos en security credentials, dentro de security credentials pulsaremos sobre Create acces key, con esto crearemos nuestras credenciales para poder conectarnos a aws desde vagrant
2. Obtención de las claves ssh  
	* Para la obtención de las claves ssh, deberemos irnos al servicio denominado EC2, en la página de dicho servicio marcaremos Key Pairs, una vez en la página de Key Pairs aparecerá una nueva ventana, en dicha ventana pincharemos en Create Key Pair, cuando pinchemos nos solicitará un nombre, una vez dado el nombre se creará la clave y el navegador la descargará de forma automática. En nuestro caso ese archivo descargado a sido almacenado en la carpeta .ssh
3. Apertura de los puertos
	En el servicio EC2 en el apartado security groups, deberemos abrir los puertos para la conexión ssh y los puertos que puedan necesitar nuestros servicios

#### Creación de los archivos de provisionamiento

Deberemos tener en cuenta que para que ansible se pueda conectar por ssh, deberemos crear un archivo de configuración añadiendo la siguiente línea

		[ssh_connection]
		control_path=%(directory)s/%%h-%%p-%%r
Una vez creado el archivo de configuración, deberemos añadir en los playbooks las siguientes líneas

		vars:
 			token_bot: "{{ lookup('env','token_bot') }}"
 			DATABASE_URL: "{{ lookup('env','DATABASE_URL')}}"
Una vez añadidas estas líneas en el archivo, ya solo queda rellenar el playbook con las tareas que deseemos que se ejecuten

#### Creación de los archivos de despliegue  

Para hacer el despliegue usaremos fabric python. Los archivos de despliegue se estructura en funciones, donde cada función lanzará, parará o reiniciará un servicio o unos tests o la instalación de los requirements. Dentro de cada función lanzará los programas necesarios para cumplir los objetivos de la función.  
La ejecución de los comandos que necesiten permisos de root, se ejecutaran con sudo y los que no se ejecutarán con run. Para lanzar los programas en background usaremos

				sudo(' screen -d -m python3 /vagrant/manage.py runserver 0.0.0.0:80 ', pty=False)

#### Creación de las máquinas en vagrant  

En este apartado explicaremos como crearemos una máquina para uno de nuestros servicos, os recordamos que nuestra aplicación se compone de tres servicios, uno que hace frontend, otro que hace de backend y otro servicio que alberga los servidores de redis y rabbitmq.     
Para crear una máquina  aws en vagrant, debemos instalar vagrant-aws. En este [enlace](https://github.com/mitchellh/vagrant-aws) explica como instalar y configurar la máquina en vagrant.    
Una vez instalado el plugin, debemos declarar tantas máquinas como vayamos a usar, las máquinas se declaran asi:

				config.vm.define "django" do |django|
Una vez declaradas crearemos un proveedor dentro de las máquinas que acabamos de definir, en nuestro caso como queremos usar vagrant-aws la declaramos de la siguiente forma:

				django.vm.provider :aws do |aws, override|

Dentro del proveedor configuraremos los parámetros que nosotros deseemos, la tabla de parámetros configurables la podemos ver [aquí](https://github.com/mitchellh/vagrant-aws)

				aws.access_key_id = "access key " creada en el punto 1 del apartado Configuración de red y obtención de credenciales
				aws.secret_access_key = "access key " creada en el punto 1 del apartado Configuración de red y obtención de credenciales
				aws.keypair_name = "nombre de la clave ssh que hemos creado en el punto 2 del apartado Configuración de red y obtención de credenciales"
				aws.subnet_id = "subnet-1fda5b30" Subred que hemos creado
				aws.private_ip_address="172.31.80.100" Ip dentro de la subred
				aws.security_groups = ["sg-89b65ffd"] Grupo de seguridad, se crea por defecto
				aws.region =  "us-east-1" Region que te han asigando
				aws.instance_type= 't2.micro'
				aws.ami = "Distribución de so, que deseemos"
				override.ssh.username = "ubuntu"
				override.ssh.private_key_path =  path de donde has almacenado la clave ssh  

Como último paso será crear un makefile, que automatice todos los pasos anteriormente comentados

#### Instrucciones de ejecución
Uso del makefile:
1. Make desplegar: Despliega la aplicación y la provisionamiento
2. Make install: Hace el despliegue, ejecutando los test e instalando las dependencias
3. Make provisionar: Provisiona las maquinas

Despliegue final: ec2-52-90-176-88.compute-1.amazonaws.com

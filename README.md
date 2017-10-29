# Buscador de datos médicos  
[![Build Status](https://travis-ci.org/AntonioAlcM/tfg_ugr.svg?branch=master)](https://travis-ci.org/AntonioAlcM/tfg_ugr)  

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

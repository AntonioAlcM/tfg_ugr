from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.http import JsonResponse
from django.core import serializers
import json
import requests
import urllib
import time
from json import dumps
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import os
from Buscador.tasks import obtenerJson
from django.views.generic import View
class buscador(View):
    def __init__(self):
        self.data_ncbi={}
        self.data_array={}
        self.palabra_clave=""
        self.url_ncbi=""
        self.url_array=""
        self.historial_busqueda=[]
        self.expedientes=[]
    def buscar(self,request):
        if request.method == "POST":
            self.palabra_clave=request.POST['search']
            self.palabra_clave=self.palabra_clave.replace(' ','%20')
            self.url_ncbi = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term={}&datetype=edat&retmax=10&usehistory=y&retmode=json'.format(self.palabra_clave)
            self.url_array = 'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments?keywords={}'.format(self.palabra_clave)
            self.data_ncbi=obtenerJson.apply_async(kwargs={'url': self.url_ncbi})
            self.data_array = obtenerJson.apply_async(kwargs={'url': self.url_array})
            self.historial_busqueda.append(self.data_ncbi)
            self.historial_busqueda.append(self.data_array)
            self.expedientes=self.obtenerExpedientes(self.data_ncbi)
            return render(request,'listarBusqueda.html')
        else:
            return render(request,'listarBusqueda.html')

    def obtenerExpedientes(self,resultados_busqueda):
        resultados=[]
        while resultados_busqueda.status == 'PENDING':
            time.sleep(2)
        for i in resultados_busqueda.get()['esearchresult']['idlist']:
            url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id={}&retmode=json'.format(i)
            resultados.append(obtenerJson.apply_async( kwargs={'url': url}))
        return resultados
    def enviarDatos(self,request):
        print(self.data_ncbi)
        informacion = tratamientosDatos(self.expedientes,self.data_array)
        lista=[]
        while len(self.expedientes) == 0:
            time.sleep(2)
        lista.append(informacion.almacenar_datos_visualizacion_ncbi())
        lista.append(informacion.almacenar_datos_visualizacion_array())
        print(lista)
        return  JsonResponse(lista, safe=False)
#def busqueda_avanzada(palabra_clave, tecnologia_secuenciacion,localizacion, organismo, base_datos):
#	if (base_datos=="ncbi"):
class tratamientosDatos():
    def __init__(self, resultados_ncbi, resultados_array):
        self.datos_ncbi=resultados_ncbi[:]
        self.resultados_array=resultados_array
    def almacenar_datos_visualizacion_array(self):
        visualizacion=[]
        for i in self.resultados_array.get()['experiments']['experiment']:
            visualizacion.append({'id': i['id'],
            'accession': i['accession'],
            'name': i['name'], 'releasedate': i['releasedate'],
             'description': i['description'][0]['text'],'bd': 'arrayexpress' })
        return visualizacion
    def almacenar_datos_visualizacion_ncbi(self):
        visualizacion=[]
        tam_list=len(self.datos_ncbi)
        for i in range(0,tam_list):
            identificador=self.datos_ncbi[i].get()['result']['uids'].pop()
            visualizacion.append({'id': identificador,
            'accession': self.datos_ncbi[i].get()['result'][identificador]['accession'],
             'name':  self.datos_ncbi[i].get()['result'][identificador]['title'],
              'releasedate': self.datos_ncbi[i].get()['result'][identificador]['pdat'],
               'description':  self.datos_ncbi[i].get()['result'][identificador]['summary'],
               'bd': 'ncbi_gds'})
        return visualizacion


def devuelve_status(request):
    opcional={"status": "OK"}
    return  JsonResponse(opcional, safe=False)

def probando_REST(request):
    if request.method == 'GET':
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer&reldate=60&datetype=edat&retmax=10&usehistory=y&retmode=json'
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        opcional={"status": "OK"}
        #return  JsonResponse(opcional, safe=False)


def index(request):
	return render(request, 'index.html')

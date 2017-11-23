from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.http import JsonResponse
from django.core import serializers
import json
import requests
import urllib
import time
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import os
from celery.result import AsyncResult
from Buscador.tasks import obtenerJson
class buscador(object):
    def __init__(self):
         self.data_array={}
         self.palabra_clave=""
         self.url_ncbi=""
         self.url_array=""
    def buscar(self,request):
        if request.method == "POST":
            self.palabra_clave=request.POST['search']
            self.url_ncbi = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&reldate=60&datetype=edat&retmax=10&usehistory=y&retmode=json'.format(self.palabra_clave)
            self.url_array = 'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments?keywords={}&species="homo%20sapiens"'.format(self.palabra_clave)
            self.data_ncbi=obtenerJson.apply_async( kwargs={'url': self.url_ncbi})
            self.data_array = obtenerJson.apply_async(kwargs={'url': self.url_array})
            ##print (data_array)
            time.sleep(15)
            print obtenerJson.apply_async( kwargs={'url': self.url_ncbi})
            #print AsyncResult(data_ncbi).status()
            return index(request)
        else:
            return index(request)


#def busqueda_avanzada(palabra_clave, tecnologia_secuenciacion,localizacion, organismo, base_datos):
#	if (base_datos=="ncbi"):




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
        return  JsonResponse(opcional, safe=False)


def index(request):
	return render(request, 'index.html')

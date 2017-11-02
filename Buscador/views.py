from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.http import JsonResponse
from django.core import serializers
import json
import requests
import urllib
import os
from bson import json_util



def buscar():
	url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer&reldate=60&datetype=edat&retmax=10&usehistory=y&retmode=json'
	response = urllib.urlopen(url)
	data = json.loads(response.read().decode('utf-8'))
	for elemento in data['esearchresult'].items():
		print (elemento)
def devuelve_estado(request):
	status={ "status": "OK"}
	opcional={ "status": "OK", "datos": { "ruta": os.path.dirname(os.path.abspath(__file__)), "valor": {"JSON": status}}}
	return  JsonResponse(opcional, safe=False)

def index(request):
    return render(request, 'index.html')

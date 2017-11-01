from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.http import JsonResponse
from django.core import serializers
import json
import urllib.request
from bson import json_util
from functools import lru_cache



def buscar():
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer&reldate=60&datetype=edat&retmax=10000&usehistory=y&retmode=json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    print (data)

def index(request):
    buscar()
    return render(request, 'index.html')

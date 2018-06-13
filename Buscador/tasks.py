from __future__ import absolute_import, unicode_literals
from BuscadorBDMedical.celery import app as app
from celery.task import Task
from celery import shared_task
import urllib
import json
import requests
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
@app.task(bind=True)
def obtenerJson(self,url):
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    response.close()
    return data
'''
@app.task(autoretry_for=(Exception,), queue='ncbi')
def obtenerJson(url):
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    response.close()
    return data
@app.task(autoretry_for=(Exception,), queue='array')
def obtenerJsonArray(url):
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    response.close()
    return data

@app.task(autoretry_for=(Exception,), queue='default')
def devolverExpedientes(inicio,fin,cola,resultados_busqueda):
    resultados=[]
    results=[]
    for i in range(inicio,fin,500):
        url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&query_key=1&WebEnv={}&retstart={}&retmax=500&rettype=json&retmode=json'.format(resultados_busqueda,i)
        if cola=="Array":
            uids=obtenerJsonArray.apply_async(kwargs={'url': url})
        else:
            uids=obtenerJson.apply_async(kwargs={'url': url})
        test=str(uids)
        resultados.append(test)
    return resultados
'''
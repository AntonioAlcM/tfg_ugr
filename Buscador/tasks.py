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

@app.task
def obtenerJson(url):
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    response.close()
    return data
@app.task
def obtenerJsonArray(url):
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    response.close()
    return data

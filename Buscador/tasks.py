from __future__ import absolute_import, unicode_literals
from BuscadorBDMedical.celery import app as app
from celery.task import Task
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

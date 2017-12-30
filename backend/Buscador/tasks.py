from __future__ import absolute_import, unicode_literals
from celery.task import Task
from celeryconfig import appcelery
import urllib
import json
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

@appcelery.task(bind=True)
def obtenerJson(self,url):
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data

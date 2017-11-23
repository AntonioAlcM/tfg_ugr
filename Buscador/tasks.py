from __future__ import absolute_import, unicode_literals
from celery import shared_task
import urllib
import json
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
@shared_task
def obtenerJson(url):
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))

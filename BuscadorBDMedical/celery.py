from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta
from kombu import Exchange, Queue, binding

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BuscadorBDMedical.settings')
app = Celery('BuscadorBDMedical', backend='redis://localhost:6379/0', broker='redis://localhost:6379')
#broker='redis://localhost:6379'
#
app.config_from_object('django.conf:settings')
app.conf.broker_transport_options = {'visibility_timeout': 43200}
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json', 'pickle'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TASK_RESULT = 'json',
    CELERY_ENABLE_UTC= 'true',
    CELERY_TIMEZONE = 'UTC',
)

'''
default_exchange = Exchange('default', type='direct')
ncbi_exchange = Exchange('ncbi', type='direct')
array_exchange = Exchange('array', type='direct')
app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('ncbi', ncbi_exchange, routing_key='ncbi_exchange.ncbi'),
    Queue('array', array_exchange, routing_key='array_exchange.array')
)

app.conf.task_routes = {
    'app.tasks.obtenerJson': {'queue': 'ncbi'},
    'app.tasks.obtenerJsonArray': {'queue': 'array'},
    'app.tasks.devolverExpedientes': {'queue': 'default'}
}
'''
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BuscadorBDMedical.settings')
app = Celery('BuscadorBDMedical')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    BROKER_URL="amqp://guest:guest@localhost//",
    CELERY_RESULT_BACKEND = 'redis://guest@localhost/0',

)

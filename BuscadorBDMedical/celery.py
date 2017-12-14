from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BuscadorBDMedical.settings')
app = Celery('BuscadorBDMedical''BuscadorBDMedical', backend='redis://127.0.0.1:6379/0', broker='amqp://guest:guest@localhost//')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json', 'pickle'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TASK_RESULT_EXPIRES = timedelta(weeks=1)
)

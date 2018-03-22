from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BuscadorBDMedical.settings')
app = Celery('BuscadorBDMedical', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json', 'pickle'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TASK_RESULT = 'json',
    CELERY_TASK_RESULT_EXPIRES = timedelta(days=1),
    CELERY_ENABLE_UTC= 'true',
    CELERY_TIMEZONE = 'UTC',
)

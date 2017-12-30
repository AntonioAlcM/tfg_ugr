from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta


appcelery = Celery('BuscadorBDMedical''BuscadorBDMedical', backend='redis://172.31.80.102:6379/0', broker='amqp://invitado:invitado@172.31.80.102//')

appcelery.autodiscover_tasks(['Buscador.tasks.obtenerJson'], force=True)
appcelery.conf.update(
        CELERY_ACCEPT_CONTENT = ['json', 'pickle'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TASK_RESULT = 'json',
    CELERY_TASK_RESULT_EXPIRES = timedelta(weeks=1),
    CELERY_ENABLE_UTC= 'true',
    CELERY_TIMEZONE = 'UTC',
)

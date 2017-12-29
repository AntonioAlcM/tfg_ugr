from __future__ import absolute_import, unicode_literals
from celery import Celery
from datetime import timedelta


app = Celery('BuscadorBDMedical''BuscadorBDMedical', backend='redis://192.168.56.102:6379/0', broker='amqp://invitado:invitado@192.168.56.102//')

app.autodiscover_tasks(['Buscador.tasks.obtenerJson'], force=True)
app.conf.update(
        CELERY_ACCEPT_CONTENT = ['json', 'pickle'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TASK_RESULT = 'json',
    CELERY_TASK_RESULT_EXPIRES = timedelta(weeks=1),
    CELERY_ENABLE_UTC= 'true',
    CELERY_TIMEZONE = 'UTC/Madrid',
)

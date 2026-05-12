from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery
import ssl

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AntaBackEnd.settings')

app = Celery("AntaBackEnd")

app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

app.config_from_object('django.conf:settings', namespace='CELERY')

"""app.conf.broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE
}

app.conf.redis_backend_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE
}"""

app.autodiscover_tasks()
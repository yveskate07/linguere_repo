import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AntaBackEnd.settings')

app = Celery("AntaBackEnd")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def send_mail():
    pass
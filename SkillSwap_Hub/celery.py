import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SkillSwap_Hub.settings')

app = Celery('SkillSwap_Hub')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Create your tasks here
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desktop.settings')

app = Celery('tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def add(x, y):
    return x + y

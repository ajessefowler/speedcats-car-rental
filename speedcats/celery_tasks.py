# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'speedcats.settings')

app = Celery('speedcats')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'], CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task
def set_vehicle_as_reserved(vehicle):
    vehicle.status = 'r'
    vehicle.save()

@app.task
def set_vehicle_as_available(vehicle, store):
    vehicle.status = 'a'
    vehicle.store = store
    vehicle.save()

'''
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
'''
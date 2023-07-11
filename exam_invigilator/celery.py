from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_invigilator.settings')

# Create the Celery app
app = Celery('exam_invigilator')
app.conf.enable_utc=False



# Load the Django settings
app.config_from_object(settings, namespace='CELERY')

# Discover tasks in all registered Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')

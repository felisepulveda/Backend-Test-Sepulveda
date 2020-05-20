from __future__ import absolute_import
 
import os
 
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Almuerzos.settings') 
 
from django.conf import settings  
 
app = Celery('CeleryApp') 
 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) 
CELERY_BROKER_URL = getattr(settings, 'CELERY_BROKER_URL', None)
app.conf.update(
    #BROKER_URL = 'django://',
    BROKER_URL = CELERY_BROKER_URL,  
)

app.conf.timezone = 'America/Santiago'
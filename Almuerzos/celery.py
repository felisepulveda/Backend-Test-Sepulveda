from __future__ import absolute_import
 
import os
 
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Almuerzos.settings') 
 
from django.conf import settings  

# Archivo de configuracion de celery para gestionar tareas de forma asincrona,
# con el uso de crontabs para automatizar la ejecucion de tareas

 
app = Celery('CeleryApp') 
 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) 
CELERY_BROKER_URL = getattr(settings, 'CELERY_BROKER_URL', None)
app.conf.update(
    #BROKER_URL = 'django://',
    BROKER_URL = CELERY_BROKER_URL,  
    CELERYBEAT_SCHEDULE={
        'borrar_db': {
            'task': 'gestionAlmuerzos.tasks.drop',
            'schedule': crontab(minute=15, hour=6, day_of_week='mon,tue,wed,thu,fri,sat,sun')
        },
        'enviar_reminders': {
            'task': 'gestionAlmuerzos.tasks.sendReminder',
            'schedule': crontab(minute=15, hour=7, day_of_week='mon,tue,wed,thu,fri,sat,sun')
        }
    }


)

app.conf.timezone = 'America/Santiago'
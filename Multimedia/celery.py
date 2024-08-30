# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el entorno predeterminado para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Multimedia.settings')

# Crea una nueva instancia de Celery
app = Celery('Multimedia')

# Carga la configuración de Django en Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks.py en las aplicaciones de Django
app.autodiscover_tasks()

from __future__ import absolute_import, unicode_literals

# Importa el archivo Celery
from .celery import app as celery_app

# Este comando hace que celery se cargue con Django
__all__ = ('celery_app',)

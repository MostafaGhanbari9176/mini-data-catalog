from .celery import app as celery_app

# Django automatically loads Celery when it starts
__all__ = ('celery_app',)
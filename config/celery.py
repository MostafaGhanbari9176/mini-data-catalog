import os
from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Create Celery app
app = Celery("config")

# Load settings from Django settings.py using CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all Django apps
app.autodiscover_tasks()

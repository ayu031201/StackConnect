import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qna.settings')
app = Celery('qna')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_new_questions': {
        'task': 'content.tasks.get_new_questions',
        'schedule': crontab(hour=0, minute=0),
    },
}

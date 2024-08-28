from celery import Celery
from celery.schedules import crontab

# Create a Celery instance
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
)

# Update Celery configuration
celery_app.conf.update(
    task_routes={
        'tasks.send_overdue_reminders': {'queue': 'reminders'},
        'tasks.generate_weekly_reports': {'queue': 'reports'},
    },
    beat_schedule={
        'send-overdue-reminders-daily': {
            'task': 'tasks.send_overdue_reminders',
            'schedule': crontab(minute='0', hour='0'),  # Daily at midnight
        },
        'generate-weekly-reports': {
            'task': 'tasks.generate_weekly_reports',
            'schedule': crontab(minute='0', hour='0', day_of_week='sunday'),  # Weekly on Sunday
        },
    },
    result_expires=3600,
)
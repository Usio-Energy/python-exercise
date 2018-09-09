redis-server
celery -A celery_worker worker -l info
celery -A celery_worker beat -l info

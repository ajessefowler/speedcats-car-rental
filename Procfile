web: gunicorn speedcats.wsgi --log-file -
worker: celery -A speedcats.celery_tasks worker -B --loglevel=info
from celery import Celery
from phoenix.optimizers import cache_utils
import os

redis_params = cache_utils.get_redis_params()

redis_url = redis_params.get('redis_url')
redis_hash_bucket = 'celery-test'

celery_app = Celery('tasks', broker=redis_url, backend=redis_url)
celery_app.autodiscover_tasks(['phoenix.tasks'])

if __name__ == "__main__":
    celery_app.start()

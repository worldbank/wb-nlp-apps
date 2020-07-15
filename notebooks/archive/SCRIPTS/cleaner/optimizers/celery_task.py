from celery import Celery
import redis
import random
import cache_utils

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

redis = redis.Redis()
redis_hash_bucket = 'celery-test'


def get_from_bucket(bucket_id, key):
    return redis.hget(bucket_id, key)

@cache_utils.redis_cacher
def compute_squared(x, **kwargs):
    print('Not from cache!')
    return x**2

@app.task
def read_and_store():
    d = random.randint(0, 100)
    sq = compute_squared(d, argument_hash=d)
    return d, cache_utils.store_to_bucket(redis_hash_bucket, d, sq)

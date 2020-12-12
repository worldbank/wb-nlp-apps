# Implement redis cacher
'''This module wraps the redis server to serve primarily as a caching service.

# # If not yet present, instantiate a docker instance of redis using the following command...
# docker run --name=wb-nlp-redis --publish=6379:6379 --hostname=redis --restart=on-failure --detach redis:latest
# docker stop wb-nlp-redis
# WB_NLP_REDIS_HOSTNAME=localhost python

'''
import os
import json
import joblib
import redis


def get_redis_params():
    '''Extracts redis params from env but fallsback to container host if not present.
    '''

    redis_host = os.environ.get(
        'WB_NLP_REDIS_HOSTNAME', 'redis')  # 'localhost')
    redis_port = os.environ.get('WB_NLP_REDIS_PORT', '6379')
    redis_db = os.environ.get('WB_NLP_REDIS_DB', '0')
    redis_url = f'redis://{redis_host}:{redis_port}/{redis_db}'

    return dict(
        redis_host=redis_host,
        redis_port=redis_port,
        redis_db=redis_db,
        redis_url=redis_url
    )


def get_redis():
    '''Creates a redis instance based on the params set.
    '''
    redis_params = get_redis_params()
    cache = redis.Redis(
        host=redis_params.get('redis_host'),
        port=redis_params.get('redis_port'),
        db=redis_params.get('redis_db'),
    )

    return cache


CACHE_HASH_BUCKET = 'cache-hashes'

try:
    redis_cache = get_redis()
    redis_cache.hset('test', '1029', '1029')
except redis.ConnectionError:
    # Fallback to localhost
    os.environ['WB_NLP_REDIS_PORT'] = 'localhost'
    redis_cache = get_redis()


def get_from_bucket(bucket_id, key):
    '''Wrapper function for hget.
    '''
    return redis_cache.hget(bucket_id, key)


def store_to_bucket(bucket_id, key, value):
    '''Wrapper function for hset.
    '''
    return redis_cache.hset(bucket_id, key, value)


def get_func_fullname(func):
    # derived from joblib: https://github.com/joblib/joblib/blob/master/joblib/memory.py
    """Compute the part of part associated with a function."""
    modules, funcname = joblib.func_inspect.get_func_name(func)
    modules.append(funcname)

    return os.path.join(*modules)


def get_argument_hash(func, args, kwargs, ignore_list=None):
    if ignore_list is None:
        ignore_list = []

    argument_hash = joblib.hashing.hash(
        joblib.func_inspect.filter_args(
            func, ignore_list, args, kwargs),
        # (self.mmap_mode is not None) # mmap_mode is None by default
        coerce_mmap=False
    )

    return argument_hash


def redis_cacher(func):
    # TODO: add a namespace
    '''
    Must be used only to cache string in the meantime.
    For unhashed key, specify the `argument_hash` kwargs.
    '''
    def wrapper(*args, **kwargs):

        argument_hash = kwargs.get(
            'argument_hash', get_argument_hash(func, args, kwargs))
        func_id = get_func_fullname(func)

        store_to_bucket(CACHE_HASH_BUCKET, func_id, 0)

        fromcache = redis_cache.hget(func_id, argument_hash)

        if fromcache is None:
            value = func(*args, **kwargs)
            tocache = json.dumps(value)

            # print(func_id, argument_hash)
            redis_cache.hset(func_id, argument_hash, tocache)
        else:
            # Decode since redis returns a byte encoded string
            fromcache = fromcache.decode('utf-8')
            value = json.loads(fromcache)

        return value

    return wrapper

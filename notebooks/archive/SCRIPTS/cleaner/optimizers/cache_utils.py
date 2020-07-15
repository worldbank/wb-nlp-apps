# Implement redis cacher
import joblib
import os
import json
import redis

# docker run --name=wb-nlp-redis --publish=6379:6379 --hostname=redis --restart=on-failure --detach redis:latest
# docker stop wb-nlp-redis
CACHE_HASH_BUCKET = 'cache-hashes'
redis_cache = redis.Redis(host='localhost', port=6379, db=0)


def store_to_bucket(bucket_id, key, value):
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
        coerce_mmap=False # (self.mmap_mode is not None) # mmap_mode is None by default
    )

    return argument_hash


def redis_cacher(func):
    # TODO: add a namespace
    '''
    Must be used only to cache string in the meantime.
    '''
    def wrapper(*args, **kwargs):

        argument_hash = kwargs.get('argument_hash', get_argument_hash(func, args, kwargs))
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